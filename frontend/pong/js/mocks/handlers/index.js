import { handlers as friendsHandlers } from "./friends";
import { handlers as healthHandlers } from "./health";
import { handlers as usersHandlers } from "./users";
import { handlers as webSocketHandlers } from "./webSocket";

export const handlers = [
  ...healthHandlers,
  ...usersHandlers,
  ...friendsHandlers,
  ...webSocketHandlers,
];
