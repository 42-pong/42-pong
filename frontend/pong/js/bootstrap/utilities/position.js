import { setClassNames } from "../../utils/elements/setClassNames";

const setFixed = (element) => {
  return setClassNames(element, "position-fixed");
};

const setRelative = (element) => {
  return setClassNames(element, "position-relative");
};

const setAbsolute = (element) => {
  return setClassNames(element, "position-absolute");
};

const setTop = (element, position = 0) => {
  return setClassNames(element, `top-${position}`);
};

const setBottom = (element, position = 0) => {
  return setClassNames(element, `bottom-${position}`);
};

const setStart = (element, position = 0) => {
  return setClassNames(element, `start-${position}`);
};

const setEnd = (element, position = 0) => {
  return setClassNames(element, `end-${position}`);
};

const setTranslateMiddle = (element) => {
  return setClassNames(element, "translate-middle");
};

export const BootstrapPosition = {
  setFixed,
  setRelative,
  setAbsolute,
  setTop,
  setBottom,
  setStart,
  setEnd,
  setTranslateMiddle,
};
