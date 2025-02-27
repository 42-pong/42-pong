import { handlers as blocksHandlers } from "./blocks";
import { handlers as friendsHandlers } from "./friends";
import { handlers as healthHandlers } from "./health";
import { handlers as participationsHandlers } from "./participations";
import { handlers as tokenHandlers } from "./token";
import { handlers as tournamentsHandlers } from "./tournaments";
import { handlers as usersHandlers } from "./users";
import { handlers as webSocketHandlers } from "./webSocket";

export const handlers = [
  ...friendsHandlers,
  ...blocksHandlers,
  ...healthHandlers,
  ...participationsHandlers,
  ...tokenHandlers,
  ...tournamentsHandlers,
  ...usersHandlers,
  ...webSocketHandlers,
];
