import { UserConstants } from "../../constants/UserConstants";

export const isValidDisplayName = (name) => {
  if (!(typeof name === "string")) return false;

  return UserConstants.DisplayName.VALID_REGEX().test(name);
};
