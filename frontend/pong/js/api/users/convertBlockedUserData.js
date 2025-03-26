import { convertUserData } from "./convertUserData";

export const convertBlockedUserData = (blockedUserData) => {
  const { blocked_user: userData } = blockedUserData;

  return convertUserData(userData);
};
