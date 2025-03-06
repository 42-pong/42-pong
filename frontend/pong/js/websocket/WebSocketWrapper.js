import { Endpoints } from "../constants/Endpoints";
import { WebSocketEnums } from "../enums/WebSocketEnums";
import { customDelay } from "../utils/customDelay";

export class WebSocketWrapper {
  #socket;
  #handlers;
  #onClose;
  #onError;
  #onMessage;
  #status;

  constructor({ status, onClose, onError }) {
    this.#status = status;
    this.#onClose = onClose;
    this.#onError = onError;
    this.#onMessage = (event) => {
      const { category, payload } = JSON.parse(event.data);
      for (const handler of this.#handlers[category])
        handler(payload);
    };
    this.init(null);
  }

  init(socket) {
    this.#socket = socket;
    this.#handlers = {};
    for (const category of Object.values(WebSocketEnums.Category))
      this.#handlers[category] = new Set();

    this.attachHandler(WebSocketEnums.Category.LOGIN, (payload) => {
      const { status, online_friend_ids } = payload;
      if (status !== "OK") return;
      const newData = {};
      for (const online_friend_id of online_friend_ids) {
        newData[online_friend_id] = { isOnline: true };
      }
      this.#status.updateData(newData);
    });
    this.attachHandler(WebSocketEnums.Category.STATUS, (payload) => {
      const { user_id, online } = payload;
      this.#status.updateData({ [user_id]: { isOnline: online } });
    });
  }

  get readyState() {
    return this.#socket.readyState;
  }

  send(category, payload) {
    if (this.#socket === null) return;
    this.#socket.send(JSON.stringify({ category, payload }));
  }

  async connect() {
    const socket = new WebSocket(Endpoints.WEBSOCKET);
    socket.addEventListener("close", this.#onClose);
    socket.addEventListener("error", this.#onError);
    socket.addEventListener("message", this.#onMessage);

    const isConnected = await isOpenWebSocket(socket);
    if (isConnected) this.init(socket);
    return isConnected;
  }

  close() {
    if (this.#socket === null) return;

    this.#socket.removeEventListener("close", this.#onClose);
    this.#socket.removeEventListener("error", this.#onError);
    this.#socket.removeEventListener("message", this.#onMessage);

    this.#socket.close();
    this.init(null);
  }

  attachHandler(category, handler) {
    this.#handlers[category].add(handler);
  }

  detachHandler(category, handler) {
    this.#handlers[category].delete(handler);
  }
}

// WebSocket の接続状態は、次の四つのいずれかの値を持つ
// - CONNECTING
// - OPEN
// - CLOSING
// - CLOSED
//
// 接続状態が OPEN であるかを、何回か繰り返して確認する関数
// - 引数 checkLimit と関係なく、必ず一回はチェック
// - 引数 checkLimit が 3 なら 3回チェック
// - 繰り返すたびに、間の時間を 2倍で伸ばしていく
//   ex) 100ms -> 200ms -> 400ms -> 800ms
const isOpenWebSocket = async (socket, checkLimit = 5) => {
  const DELAY_INTERVAL_INIT = 100;

  if (!socket) return false;

  try {
    let delayInterval = DELAY_INTERVAL_INIT;
    let checkCount = 0;

    while (true) {
      switch (socket.readyState) {
        case WebSocket.CONNECTING:
          break;
        case WebSocket.OPEN:
          return true;
        // case WebSocket.CLOSING:
        // case WebSocket.CLOSED:
        default:
          return false;
      }

      ++checkCount;
      if (checkCount >= checkLimit) break;

      await customDelay(delayInterval);
      delayInterval *= 2;
    }
  } catch (error) {}

  return false;
};
