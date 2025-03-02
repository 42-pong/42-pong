import { BootstrapDisplay } from "../../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../../bootstrap/utilities/flex";
import { BootstrapSpacing } from "../../../bootstrap/utilities/spacing";
import { BootstrapText } from "../../../bootstrap/utilities/text";
import { createAvatarImage } from "../../user/createAvatarImage";
import { formatUserInfo } from "../../user/formatUserInfo";
import { createElement } from "../createElement";

export const createNameplate = (user, avatarHeight = "") => {
  const { nameTagText, avatarPathname, avatarAlt } =
    formatUserInfo(user);

  const avatar = createAvatarImage({
    pathname: avatarPathname,
    alt: avatarAlt,
    height: avatarHeight,
  });
  const nameTag = createElement("span", {
    textContent: nameTagText,
  });
  BootstrapText.setTextTruncate(nameTag);

  const nameplate = createElement("div");
  BootstrapDisplay.setFlex(nameplate);
  BootstrapFlex.setAlignItemsCenter(nameplate);
  BootstrapSpacing.setGap(nameplate);
  nameplate.append(avatar, nameTag);
  return nameplate;
};
