import { setClassNames } from "../../utils/elements/setClassNames";

const setPrimary = (element) => {
  return setClassNames(element, "btn", "btn-primary");
};

const setSecondary = (element) => {
  return setClassNames(element, "btn", "btn-secondary");
};

const setSuccess = (element) => {
  return setClassNames(element, "btn", "btn-success");
};

const setDanger = (element) => {
  return setClassNames(element, "btn", "btn-danger");
};

const setOutlinePrimary = (element) => {
  return setClassNames(element, "btn", "btn-outline-primary");
};

const setOutlineSecondary = (element) => {
  return setClassNames(element, "btn", "btn-outline-secondary");
};

const setOutlineDanger = (element) => {
  return setClassNames(element, "btn", "btn-outline-danger");
};

const setSmall = (element) => {
  return setClassNames(element, "btn", "btn-sm");
};

export const BootstrapButtons = {
  setPrimary,
  setSecondary,
  setSuccess,
  setDanger,
  setOutlinePrimary,
  setOutlineSecondary,
  setOutlineDanger,
  setSmall,
};
