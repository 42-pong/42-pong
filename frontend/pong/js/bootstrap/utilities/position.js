import { setClassNames } from "../../utils/elements/setClassNames";

const setFixed = (element) => {
  return setClassNames(element, "position-fixed");
};

const setBottom = (element) => {
  return setClassNames(element, "bottom-0");
};

const setEnd = (element) => {
  return setClassNames(element, "end-0");
};

export const BootstrapPosition = {
  setFixed,
  setBottom,
  setEnd,
};
