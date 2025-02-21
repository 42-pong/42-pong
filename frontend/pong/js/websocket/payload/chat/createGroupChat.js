import { WebSocketEnums } from "../../../enums/WebSocketEnums";

export const createGroupChat = ({ fromId, tournamentId, content }) =>
  Object.freeze({
    type: WebSocketEnums.Chat.Type.GROUP_CHAT,
    data: {
      from: fromId,
      to: tournamentId,
      content,
    },
  });
