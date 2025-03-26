import { delay } from "msw";
import { WebSocketEnums } from "../../../enums/WebSocketEnums";
import { sendTournament } from "./sendPayloads";

const TEST_DEFAULT_ID = 42;
const TEST_ID_MATCH_TRANSITION = 44;

export const tournamentPayloadHandler = async (client, payload) => {
  const { type, data } = payload;
  switch (type) {
    case WebSocketEnums.Tournament.Type.JOIN: {
      const { tournament_id } = data;
      sendTournament(client, WebSocketEnums.Tournament.Type.JOIN, {
        status: "OK",
        tournament_id: tournament_id ?? TEST_DEFAULT_ID,
      });

      if (tournament_id === TEST_ID_MATCH_TRANSITION) {
        await delay(1000);
        sendTournament(
          client,
          WebSocketEnums.Tournament.Type.ASSIGNED,
          {
            match_id: 1,
          },
        );
      }
      break;
    }
    case WebSocketEnums.Tournament.Type.LEAVE:
      break;
    default:
      break;
  }
};
