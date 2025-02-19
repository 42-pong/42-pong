import { WebSocketEnums } from "../../../enums/WebSocketEnums";

export const createJoin = ({ joinType, tournamentId, displayName }) =>
  Object.freeze({
    type: WebSocketEnums.Tournament.Type.JOIN,
    data: {
      join_type: joinType,
      tournament_id: tournamentId,
      participation_name: displayName,
    },
  });
