import { BootstrapBorders } from "../../../bootstrap/utilities/borders";
import { BootstrapDisplay } from "../../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../../bootstrap/utilities/flex";
import { BootstrapSpacing } from "../../../bootstrap/utilities/spacing";
import { BootstrapText } from "../../../bootstrap/utilities/text";
import { Endpoints } from "../../../constants/Endpoints";
import { createElement } from "../createElement";
import { setHeight } from "../style/setHeight";

export const createNameplate = (user, avatarHeight = "") => {
  const avatar = new Image();
  avatar.src = Endpoints.create(user.avatar).href;
  avatar.alt = `${user.displayName}#${user.username}'s avatar`;
  if (avatarHeight) setHeight(avatar, avatarHeight);
  BootstrapBorders.setRoundedCircle(avatar);

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
