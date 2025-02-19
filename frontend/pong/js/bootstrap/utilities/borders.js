import { setClassNames } from "../../utils/elements/setClassNames";

const setRounded = (element) => {
  return setClassNames(element, "rounded");
};

const setRoundedCircle = (element) => {
  return setClassNames(element, "rounded-circle");
};

const setDanger = (element) => {
  return setClassNames(element, "border-danger");
};

export const BootstrapBorders = {
  setRounded,
  setRoundedCircle,
  setDanger,
};
