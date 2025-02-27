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

const setJustifyContentStart = (element) => {
  return setClassNames(element, "justify-content-start");
};

const setJustifyContentCenter = (element) => {
  return setClassNames(element, "justify-content-center");
};

const setJustifyContentBetween = (element) => {
  return setClassNames(element, "justify-content-between");
};

const setJustifyContentAround = (element) => {
  return setClassNames(element, "justify-content-around");
};

const setJustifyContentEnd = (element) => {
  return setClassNames(element, "justify-content-end");
};

const setAlignItemsCenter = (element) => {
  return setClassNames(element, "align-items-center");
};

export const BootstrapFlex = {
  setFlexColumn,
  setFlexColumnReverse,
  setFlexGrow1,
  setJustifyContentStart,
  setJustifyContentCenter,
  setJustifyContentBetween,
  setJustifyContentAround,
  setJustifyContentEnd,
  setAlignItemsCenter,
};
