import { BootstrapDisplay } from "../../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../../bootstrap/utilities/flex";
import { BootstrapOverflow } from "../../../bootstrap/utilities/overflow";
import { BootstrapSpacing } from "../../../bootstrap/utilities/spacing";
import { createElement } from "../createElement";

export const createNameplate = (user) => {
  // TODO: 実際のアバターを使用
  const avatar = new Image();
  avatar.src = "https://placehold.co/30";
  avatar.alt = "sample image";

  const nameTag = createElement("span", {
    textContent: `${user.displayName}#${user.username}`,
  });
  BootstrapOverflow.setOverflowXHidden(nameTag);

  const nameplate = createElement("div");
  BootstrapDisplay.setFlex(nameplate);
  BootstrapFlex.setAlignItemsCenter(nameplate);
  BootstrapSpacing.setGap(nameplate);
  nameplate.append(avatar, nameTag);
  return nameplate;
};
