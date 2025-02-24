import { WebSocketEnums } from "../../enums/WebSocketEnums";

export const isGroupChat = (type) =>
  type === WebSocketEnums.Chat.Type.GROUP_CHAT ||
  type === WebSocketEnums.Chat.Type.GROUP_ANNOUNCEMENT;
