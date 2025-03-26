import { UserSessionManager } from "../../session/UserSessionManager";
import { hasNumericKey } from "../hasNumericKey";

export const deleteStatus = (userId) => {
  const statusData = UserSessionManager.getInstance().status.observe(
    (data) => data,
  );
  if (!hasNumericKey(statusData, userId)) return;
  delete statusData[userId];
};
