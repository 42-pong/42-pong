import { setClassNames } from "../../utils/elements/setClassNames";

const setPadding = (element) => {
  return setClassNames(element, "p-2");
};

const setGap = (element) => {
  return setClassNames(element, "gap-3");
};

export const BootstrapSpacing = {
  setPadding,
  setGap,
};
