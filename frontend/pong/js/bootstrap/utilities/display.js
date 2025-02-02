import { setClassNames } from "../../utils/elements/setClassNames";

const setFlex = (element) => {
  return setClassNames(element, "d-flex");
};

const setGrid = (element) => {
  return setClassNames(element, "d-grid");
};

export const BootstrapDisplay = {
  setFlex,
  setGrid,
};
