import { Endpoints } from "../constants/Endpoints";

export class WebSocketWrapper {
  #socket;
  #handlers;

  constructor(url) {
    this.#socket = null;
    this.#handlers = {};
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
    socket.addEventListener("open", this.onOpen.bind(this));
    socket.addEventListener("close", this.onClose.bind(this));
    socket.addEventListener("error", this.onError.bind(this));
    socket.addEventListener("message", this.onMessage.bind(this));

    const isConnected = await isOpenWebSocket(socket);
    if (isConnected) {
      this.#socket = socket;
      this.#handlers = {};
    }
    return isConnected;
  }

  // TODO: クローズコードと理由を指定できる形にする
  close() {
    if (this.#socket === null) return;
    this.#socket.close();
    this.#socket = null;
  }

  onOpen(event) {}

  onClose(event) {
    this.#socket = null;
  }

  onError(event) {
    this.close();
  }

  onMessage(event) {
    const { category, payload } = JSON.parse(event.data);
    const handler = this.#handlers[category];

    if (handler) handler(payload);
  }

  attachHandler(category, handler) {
    this.#handlers[category] = handler;
  }

  detachHandler(category) {
    delete this.#handlers[category];
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
  // TODO: utils に移動
  const delay = (timeInMilliseconds) =>
    new Promise((resolve) => setTimeout(resolve, timeInMilliseconds));

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

      await delay(delayInterval);
      delayInterval *= 2;
    }
  } catch (error) {}

  return false;
};
