import { GeneralConstants } from "../constants/GeneralConstants";

export const isValidIdStr = (str) => {
  if (!(typeof str === "string")) return false;

  const expectedId = Number.parseInt(str);
  return (
    GeneralConstants.Id.VALID_REGEX().test(str) &&
    !Number.isNaN(expectedId)
  );
};
