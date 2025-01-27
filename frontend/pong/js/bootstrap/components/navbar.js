const setNavbarExpand = (element) => {
  element.classList.add("navbar", "navbar-expand");
};

const setNavbarBrand = (element) => {
  element.classList.add("navbar-brand");
};

const setNavbarNav = (element) => {
  element.classList.add("navbar-nav");
};

export const BootstrapNavbar = {
  setNavbarExpand,
  setNavbarBrand,
  setNavbarNav,
};
