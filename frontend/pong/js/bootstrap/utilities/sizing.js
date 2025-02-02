import { setClassNames } from "../../utils/elements/setClassNames";

const setWidth50 = (element) => {
  return setClassNames(element, "w-50");
};

const setWidth100 = (element) => {
  return setClassNames(element, "w-100");
};

const setHeight50 = (element) => {
  return setClassNames(element, "h-50");
};

const setHeight100 = (element) => {
  return setClassNames(element, "h-100");
};

const setViewportHeight100 = (element) => {
  return setClassNames(element, "vh-100");
};

export const BootstrapSizing = {
  setWidth50,
  setWidth100,
  setHeight50,
  setHeight100,
  setViewportHeight100,
};
