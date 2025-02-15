import { setClassNames } from "../../utils/elements/setClassNames";

const setBlock = (element) => {
  return setClassNames(element, "d-block");
};

const setFlex = (element) => {
  return setClassNames(element, "d-flex");
};

const setGrid = (element) => {
  return setClassNames(element, "d-grid");
};

export const BootstrapDisplay = {
  setBlock,
  setFlex,
  setGrid,
};
