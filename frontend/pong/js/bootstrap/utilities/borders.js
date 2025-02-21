import { setClassNames } from "../../utils/elements/setClassNames";
import { unsetClassNames } from "../../utils/elements/unsetClassNames";

const setBorder = (element) => {
  return setClassNames(element, "border");
};

const setRounded = (element) => {
  return setClassNames(element, "rounded");
};

const setRoundedCircle = (element) => {
  return setClassNames(element, "rounded-circle");
};

const setDanger = (element) => {
  return setClassNames(element, "border-danger");
};

const unsetDanger = (element) => {
  return unsetClassNames(element, "border-danger");
};

export const BootstrapBorders = {
  setBorder,
  setRounded,
  setRoundedCircle,
  setDanger,
  unsetDanger,
};
