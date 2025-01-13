import { ws } from "msw";
import { Endpoints } from "../../constants/Endpoints";
import { WebSocketEnums } from "../../enums/WebSocketEnums";
import { matchPayloadHandler } from "../utils/websocket/matchPayloadHandler";

const mock = ws.link(Endpoints.WEBSOCKET.href);

export const handlers = [
  mock.addEventListener("connection", ({ client }) => {
    const matchState = {};
    client.addEventListener("message", (event) => {
      const { category, payload } = JSON.parse(event.data);
      switch (category) {
        case WebSocketEnums.Category.MATCH:
          matchPayloadHandler(client, payload, matchState);
          break;
        default:
          return;
      }
    });
  }),
];
