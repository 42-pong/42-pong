import { BootstrapBorders } from "../../../bootstrap/utilities/borders";
import { BootstrapDisplay } from "../../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../../bootstrap/utilities/flex";
import { BootstrapSpacing } from "../../../bootstrap/utilities/spacing";
import { BootstrapText } from "../../../bootstrap/utilities/text";
import { Endpoints } from "../../../constants/Endpoints";
import { createElement } from "../createElement";
import { setHeight } from "../style/setHeight";

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

const createAvatarImage = (params) => {
  const { pathname, alt, height } = params;

  const image = new Image();
  image.src = Endpoints.create(pathname).href;
  image.alt = alt;
  image.onerror = () => {
    image.onerror = null;
    image.src = Endpoints.USERS.defaultAvatar.href;
  };
  if (height) setHeight(image, height);
  BootstrapBorders.setRoundedCircle(image);
  return image;
};

const formatUserInfo = (user) =>
  user
    ? {
        nameTagText: `${user.displayName}#${user.username}`,
        avatarPathname: user.avatar,
        avatarAlt: `${user.displayName}#${user.username}'s avatar`,
      }
    : {
        nameTagText: "...",
        avatarPathname: Endpoints.USERS.defaultAvatar.href,
        avatarAlt: "placeholder",
      };
