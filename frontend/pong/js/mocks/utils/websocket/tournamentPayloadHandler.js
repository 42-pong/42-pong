import { sendTournament } from "./sendPayloads";

export const tournamentPayloadHandler = (client, payload) => {
  const { type, data } = payload;
  switch (type) {
    case "JOIN":
      sendTournament(client, "JOIN", {
        status: "OK",
        tournament_id: 42,
      });
      break;
    default:
      break;
  }
};
