import { BootstrapNavsTabs } from "../../../bootstrap/components/navsTabs";
import { getTextContent } from "../../i18n/lang";
import { createElement } from "../createElement";

export const createNavbarNavList = (links) => {
  const navList = createElement("ul");
  BootstrapNavsTabs.setNav(navList);

  for (const link of links) {
    const navListItem = createNavbarNavListItem(link);
    navList.appendChild(navListItem);
  }
  return navList;
};

// 引数 link は、次のような形を前提にしています。
// {
//   name: <表示名>,
//   path: <移動先のパス>,
//   ...
// }
// ex) { name: "ホーム", path: "/", ...}
const createNavbarNavListItem = (link) => {
  const linkAnchor = createElement(
    "a",
    {
      textContent: getTextContent(link.name),
    },
    {
      href: link.path,
    },
  );
  BootstrapNavsTabs.setNavLink(linkAnchor);

  const navListItem = createElement("li");
  BootstrapNavsTabs.setNavItem(navListItem);
  navListItem.appendChild(linkAnchor);
  return navListItem;
};
