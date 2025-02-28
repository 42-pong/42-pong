import { sendLogin } from "./sendPayloads";

export const loginPayloadHandler = async (client, payload) => {
  sendLogin(client, {
    status: "OK",
    online_status_ids: [3, 4, 8, 7],
  });
};
