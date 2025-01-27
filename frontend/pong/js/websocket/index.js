import { Endpoints } from "../constants/Endpoints";
import { WebSocketWrapper } from "./WebSocketWrapper";

let globalWebSocket = null;

const initWebSocket = () => {
  if (globalWebSocket !== null) return;
  globalWebSocket = new WebSocketWrapper(Endpoints.WEBSOCKET);
};

const getWebSocket = () => {
  return globalWebSocket;
};

const clearWebSocket = () => {
  globalWebSocket.close();
  globalWebSocket = null;
};

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
const isOpenWebSocket = async (checkLimit = 5) => {
  const DELAY_INTERVAL_INIT = 100;
  // TODO: utils に移動
  const delay = (timeInMilliseconds) =>
    new Promise((resolve) => setTimeout(resolve, timeInMilliseconds));

  try {
    let delayInterval = DELAY_INTERVAL_INIT;
    let checkCount = 0;

    while (true) {
      switch (globalWebSocket.readyState) {
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

export {
  initWebSocket,
  getWebSocket,
  clearWebSocket,
  isOpenWebSocket,
};
