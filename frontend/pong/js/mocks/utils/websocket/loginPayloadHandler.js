import { sendLogin } from "./sendPayloads";

export const loginPayloadHandler = (client) => {
  sendLogin(client, {
    status: "OK",
    online_status_ids: [],
  });
};
