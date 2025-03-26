import { setClassNames } from "../../utils/elements/setClassNames";

const setLight = (element) => {
  return setClassNames(element, "bg-light");
};

const setDarkSubtle = (element) => {
  return setClassNames(element, "bg-dark-subtle");
};

export const BootstrapBackground = {
  setLight,
  setDarkSubtle,
};
