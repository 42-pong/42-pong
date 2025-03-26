import { sendLogin } from "./sendPayloads";

export const loginPayloadHandler = (client) => {
  sendLogin(client, {
    status: "OK",
    online_friend_ids: [],
  });
};
