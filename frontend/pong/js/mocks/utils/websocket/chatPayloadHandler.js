import { sendChat } from "./sendPayloads";

export const chatPayloadHandler = async (client, payload) => {
  const { type, data } = payload;
  switch (type) {
    case "GROUP_CHAT":
      sendChat(client, type, data);
      sendChat(client, "GROUP_CHAT", {
        from: 2,
        to: 42,
        content: `[ECHO] ${data.content}`,
      });
      break;
    default:
      break;
  }
};
