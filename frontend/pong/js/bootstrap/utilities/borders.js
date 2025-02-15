import { setClassNames } from "../../utils/elements/setClassNames";

const setRounded = (element) => {
  return setClassNames(element, "rounded");
};

const setRoundedCircle = (element) => {
  return setClassNames(element, "rounded-circle");
};

export const BootstrapBorders = {
  setRounded,
  setRoundedCircle,
};
