import { WebSocketEnums } from "../../enums/WebSocketEnums";
import { UserSessionManager } from "../../session/UserSessionManager";
import { hasNumericKey } from "../hasNumericKey";

export const requestStatus = (userId) => {
  if (!userId) return;
  const statusData = UserSessionManager.getInstance().status.observe(
    (data) => data,
  );
  if (hasNumericKey(statusData, userId)) return;
  UserSessionManager.getInstance().webSocket.send(
    WebSocketEnums.Category.STATUS,
    { user_id: userId },
  );
};
