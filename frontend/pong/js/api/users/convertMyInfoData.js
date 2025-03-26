import { convertUserData } from "./convertUserData";

export const convertMyInfoData = (userData) => {
  const { email } = userData;

  return {
    email,
    ...convertUserData(userData),
  };
};
