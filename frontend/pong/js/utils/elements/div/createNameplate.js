import { BootstrapDisplay } from "../../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../../bootstrap/utilities/flex";
import { BootstrapSpacing } from "../../../bootstrap/utilities/spacing";
import { BootstrapText } from "../../../bootstrap/utilities/text";
import { createElement } from "../createElement";
import { setHeight } from "../style/setHeight";

export const createNameplate = (user, avatarHeight = "") => {
  // TODO: 実際のアバターを使用
  const avatar = new Image();
  avatar.src = "https://placehold.co/30";
  avatar.alt = "sample image";
  if (avatarHeight) setHeight(avatar, avatarHeight);

  const nameTag = createElement("span", {
    textContent: `${user.displayName}#${user.username}`,
  });
  BootstrapText.setTextTruncate(nameTag);

  const nameplate = createElement("div");
  BootstrapDisplay.setFlex(nameplate);
  BootstrapFlex.setAlignItemsCenter(nameplate);
  BootstrapSpacing.setGap(nameplate);
  nameplate.append(avatar, nameTag);
  return nameplate;
};
