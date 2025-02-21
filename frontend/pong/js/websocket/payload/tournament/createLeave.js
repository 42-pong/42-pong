import { WebSocketEnums } from "../../../enums/WebSocketEnums";

export const createLeave = ({ tournamentId }) =>
  Object.freeze({
    type: WebSocketEnums.Tournament.Type.LEAVE,
    data: {
      tournament_id: tournamentId,
    },
  });
