import { setClassNames } from "../../utils/elements/setClassNames";

const setPrimary = (element) => {
  return setClassNames(element, "badge", "text-bg-primary");
};

const setSecondary = (element) => {
  return setClassNames(element, "badge", "text-bg-secondary");
};

const setSuccess = (element) => {
  return setClassNames(element, "badge", "text-bg-success");
};

const setDanger = (element) => {
  return setClassNames(element, "badge", "text-bg-danger");
};

const setWarning = (element) => {
  return setClassNames(element, "badge", "text-bg-warning");
};

const setInfo = (element) => {
  return setClassNames(element, "badge", "text-bg-info");
};

const setDark = (element) => {
  return setClassNames(element, "badge", "text-bg-dark");
};

const setRoundedPill = (element) => {
  return setClassNames(element, "rounded-pill");
};

export const BootstrapBadge = {
  setPrimary,
  setSecondary,
  setSuccess,
  setDanger,
  setWarning,
  setInfo,
  setDark,
  setRoundedPill,
};
