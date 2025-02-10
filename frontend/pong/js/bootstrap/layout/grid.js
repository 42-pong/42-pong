import { setClassNames } from "../../utils/elements/setClassNames";

const setContainer = (element) => {
  return setClassNames(element, "container");
};

const setRow = (element) => {
  return setClassNames(element, "row");
};

const setCol = (element, colSize, breakpoint = "") => {
  const columnClassName = breakpoint
    ? `col-${breakpoint}-${colSize}`
    : `col-${colSize}`;
  return setClassNames(element, columnClassName);
};

export const BootstrapGrid = {
  setContainer,
  setRow,
  setCol,
};
