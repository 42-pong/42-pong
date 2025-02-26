import { setClassNames } from "../../utils/elements/setClassNames";

const setFixed = (element) => {
  return setClassNames(element, "position-fixed");
};

const setTop = (element) => {
  return setClassNames(element, "top-0");
};

const setBottom = (element) => {
  return setClassNames(element, "bottom-0");
};

const setEnd = (element) => {
  return setClassNames(element, "end-0");
};

export const BootstrapPosition = {
  setFixed,
  setTop,
  setBottom,
  setEnd,
};
