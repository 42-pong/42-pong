import { setClassNames } from "../../utils/elements/setClassNames";

const setNav = (element) => {
  return setClassNames(element, "nav");
};

const setNavItem = (element) => {
  return setClassNames(element, "nav-item");
};

const setNavLink = (element) => {
  return setClassNames(element, "nav-link");
};

export const BootstrapNavsTabs = {
  setNav,
  setNavItem,
  setNavLink,
};
