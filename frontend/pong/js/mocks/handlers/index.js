import { handlers as healthHandlers } from "./health";
import { handlers as webSocketHandlers } from "./webSocket";

export const handlers = [...healthHandlers, ...webSocketHandlers];
