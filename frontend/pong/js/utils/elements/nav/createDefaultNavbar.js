import { BootstrapNavbar } from "../../../bootstrap/components/navbar";
import { BootstrapContainers } from "../../../bootstrap/layout/containers";
import { createBrandAnchor } from "../anchor/createBrandAnchor";
import { createElement } from "../createElement";
import { createNavbarNavList } from "./createNavbarNavList";

export const createDefaultNavbar = (links) => {
  const navList = createNavbarNavList(links);
  BootstrapNavbar.setNavbarNav(navList);

  const brand = createBrandAnchor();
  BootstrapNavbar.setNavbarBrand(brand);

  const navListWrapper = createElement("div");
  navListWrapper.appendChild(navList);

  const containerFluid = createElement("div");
  BootstrapContainers.setFluid(containerFluid);
  containerFluid.appendChild(brand);
  containerFluid.appendChild(navListWrapper);

  const navbar = createElement("nav");
  BootstrapNavbar.setNavbarExpand(navbar);
  navbar.appendChild(containerFluid);
  return navbar;
};
