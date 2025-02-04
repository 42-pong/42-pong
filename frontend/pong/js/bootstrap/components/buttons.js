import { setClassNames } from "../../utils/elements/setClassNames";

const setPrimary = (element) => {
  return setClassNames(element, "btn", "btn-primary");
};

const setSecondary = (element) => {
  return setClassNames(element, "btn", "btn-secondary");
};

const setOutlinePrimary = (element) => {
  return setClassNames(element, "btn", "btn-outline-primary");
};

const setOutlineSecondary = (element) => {
  return setClassNames(element, "btn", "btn-outline-secondary");
};

export const BootstrapButtons = {
  setPrimary,
  setSecondary,
  setOutlinePrimary,
  setOutlineSecondary,
};
