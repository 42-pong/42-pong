import { setClassNames } from "../../utils/elements/setClassNames";
import { unsetClassNames } from "../../utils/elements/unsetClassNames";

const setBlock = (element) => {
  return setClassNames(element, "d-block");
};

const setFlex = (element) => {
  return setClassNames(element, "d-flex");
};

const setGrid = (element) => {
  return setClassNames(element, "d-grid");
};

const setNone = (element) => {
  return setClassNames(element, "d-none");
};

const unsetNone = (element) => {
  return unsetClassNames(element, "d-none");
};

export const BootstrapDisplay = {
  setBlock,
  setFlex,
  setGrid,
  setNone,
  unsetNone,
};
