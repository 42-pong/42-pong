import { setClassNames } from "../../utils/elements/setClassNames";

const setTextCenter = (element) => {
  return setClassNames(element, "text-center");
};

const setTextTruncate = (element) => {
  return setClassNames(element, "text-truncate");
};

export const BootstrapText = {
  setTextCenter,
  setTextTruncate,
};
