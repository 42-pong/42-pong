import { Paths } from "../../../constants/Paths";
import { createElement } from "../createElement";

export const createBrandAnchor = () => {
  const brandAnchor = createElement(
    "a",
    { textContent: "Pong" },
    { href: Paths.HOME },
  );
  return brandAnchor;
};
