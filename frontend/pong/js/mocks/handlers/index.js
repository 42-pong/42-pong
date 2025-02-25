import { handlers as friendsHandlers } from "./friends";
import { handlers as healthHandlers } from "./health";
import { handlers as participationsHandlers } from "./participations";
import { handlers as tokenHandlers } from "./token";
import { handlers as usersHandlers } from "./users";
import { handlers as webSocketHandlers } from "./webSocket";

export const handlers = [
  ...friendsHandlers,
  ...healthHandlers,
  ...participationsHandlers,
  ...tokenHandlers,
  ...usersHandlers,
  ...webSocketHandlers,
];
