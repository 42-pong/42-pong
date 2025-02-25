import { setClassNames } from "../../utils/elements/setClassNames";

const setFlexColumn = (element) => {
  return setClassNames(element, "flex-column");
};

const setFlexColumnReverse = (element) => {
  return setClassNames(element, "flex-column-reverse");
};

const setFlexGrow1 = (element) => {
  return setClassNames(element, "flex-grow-1");
};

const setJustifyContentCenter = (element) => {
  return setClassNames(element, "justify-content-center");
};

const setJustifyContentAround = (element) => {
  return setClassNames(element, "justify-content-around");
};

const setAlignItemsCenter = (element) => {
  return setClassNames(element, "align-items-center");
};

export const BootstrapFlex = {
  setFlexColumn,
  setFlexColumnReverse,
  setFlexGrow1,
  setJustifyContentCenter,
  setJustifyContentAround,
  setAlignItemsCenter,
};
