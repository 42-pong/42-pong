import { setClassNames } from "../../utils/elements/setClassNames";

const setPadding = (element, size = 2) => {
  return setClassNames(element, `p-${size}`);
};

const setMargin = (element, size = 2) => {
  return setClassNames(element, `m-${size}`);
};

const setGap = (element, size = 3) => {
  return setClassNames(element, `gap-${size}`);
};

export const BootstrapSpacing = {
  setPadding,
  setMargin,
  setGap,
};
