import { setClassNames } from "../../utils/elements/setClassNames";

const setForm = (element) => {
  return setClassNames(element, "navbar", "navbar-expand");
};

const setNavbarBrand = (element) => {
  return setClassNames(element, "navbar-brand");
};

const setNavbarNav = (element) => {
  return setClassNames(element, "navbar-nav");
};

export const BootstrapNavbar = {
  setNavbarExpand,
  setNavbarBrand,
  setNavbarNav,
};
