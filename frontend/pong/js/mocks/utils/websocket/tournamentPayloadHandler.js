import { delay } from "msw";
import { WebSocketEnums } from "../../../enums/WebSocketEnums";
import { sendTournament } from "./sendPayloads";

export const tournamentPayloadHandler = async (client, payload) => {
  const { type, data } = payload;
  switch (type) {
    case WebSocketEnums.Tournament.Type.JOIN: {
      const { tournament_id } = data;
      sendTournament(client, WebSocketEnums.Tournament.Type.JOIN, {
        status: "OK",
        tournament_id: tournament_id ? tournament_id : 42,
      });
      await delay(1000);
      sendTournament(client, WebSocketEnums.Tournament.Type.RELOAD, {
        event: WebSocketEnums.Tournament.ReloadEvent.PLAYER_CHANGE,
      });
      break;
    }
    case WebSocketEnums.Tournament.Type.LEAVE:
      break;
    default:
      break;
  }
};
