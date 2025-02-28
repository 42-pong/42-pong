import { WebSocketEnums } from "../../../enums/WebSocketEnums";

const send = (client, category, payload) => {
  client.send(
    JSON.stringify({
      category: category,
      payload,
    }),
  );
};

const sendMatch = (client, stage, data) =>
  send(client, WebSocketEnums.Category.MATCH, { stage, data });

const sendTournament = (client, type, data) =>
  send(client, WebSocketEnums.Category.TOURNAMENT, { type, data });

const sendChat = (client, type, data) =>
  send(client, WebSocketEnums.Category.CHAT, { type, data });

export { sendMatch, sendTournament, sendChat };
