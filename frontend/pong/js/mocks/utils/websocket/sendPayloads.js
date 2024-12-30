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

export { sendMatch };
