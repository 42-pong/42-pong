import { setClassNames } from "../../utils/elements/setClassNames";

const setTextCenter = (element) => {
  return setClassNames(element, "text-center");
};

const setTextTruncate = (element) => {
  return setClassNames(element, "text-truncate");
};

const setFontSize = (element, size) => {
  return setClassNames(element, `fs-${size}`);
};

export const BootstrapText = {
  setTextCenter,
  setTextTruncate,
  setFontSize,
};
