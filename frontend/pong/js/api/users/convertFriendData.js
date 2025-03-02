import { convertUserData } from "./convertUserData";

export const convertFriendData = (friendData) => {
  const { friend: userData } = friendData;

  return convertUserData(userData);
};
