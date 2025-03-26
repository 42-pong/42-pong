import { setClassNames } from "../../utils/elements/setClassNames";

const setWidth25 = (element) => {
  return setClassNames(element, "w-25");
};

const setWidth50 = (element) => {
  return setClassNames(element, "w-50");
};

const setWidth75 = (element) => {
  return setClassNames(element, "w-75");
};

const setWidth100 = (element) => {
  return setClassNames(element, "w-100");
};

const setHeight25 = (element) => {
  return setClassNames(element, "h-25");
};

const setHeight50 = (element) => {
  return setClassNames(element, "h-50");
};

const setHeight75 = (element) => {
  return setClassNames(element, "h-75");
};

const setHeight100 = (element) => {
  return setClassNames(element, "h-100");
};

const setViewportHeight100 = (element) => {
  return setClassNames(element, "vh-100");
};

const setMaxHeight100 = (element) => {
  return setClassNames(element, "mh-100");
};

export const BootstrapSizing = {
  setWidth25,
  setWidth50,
  setWidth75,
  setWidth100,
  setHeight25,
  setHeight50,
  setHeight75,
  setHeight100,
  setViewportHeight100,
  setMaxHeight100,
};
