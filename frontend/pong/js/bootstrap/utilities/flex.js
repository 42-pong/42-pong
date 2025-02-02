import { setClassNames } from "../../utils/elements/setClassNames";

const setFlexColumn = (element) => {
  return setClassNames(element, "flex-column");
};

const setFlexGrow1 = (element) => {
  return setClassNames(element, "flex-grow-1");
};

const setJustifyContentCenter = (element) => {
  return setClassNames(element, "justify-content-center");
};

const setAlignItemsCenter = (element) => {
  return setClassNames(element, "align-items-center");
};

export const BootstrapFlex = {
  setFlexColumn,
  setFlexGrow1,
  setJustifyContentCenter,
  setAlignItemsCenter,
};
