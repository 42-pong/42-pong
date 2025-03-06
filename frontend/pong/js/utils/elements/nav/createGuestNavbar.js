import { BootstrapNavbar } from "../../../bootstrap/components/navbar";
import { BootstrapContainers } from "../../../bootstrap/layout/containers";
import { UserProfileHeader } from "../../../components/user/UserProfileHeader";
import { createBrandAnchor } from "../anchor/createBrandAnchor";
import { createElement } from "../createElement";

export const createGuestNavbar = () => {
  const brand = createBrandAnchor();
  BootstrapNavbar.setNavbarBrand(brand);

  const profileHeader = new UserProfileHeader();

  const containerFluid = createElement("div");
  BootstrapContainers.setFluid(containerFluid);
  containerFluid.append(brand, profileHeader);

  const navbar = createElement("nav");
  BootstrapNavbar.setNavbarExpand(navbar);
  navbar.appendChild(containerFluid);
  return navbar;
};
