import { BootstrapBadge } from "../../../bootstrap/components/badge";
import { BootstrapBorders } from "../../../bootstrap/utilities/borders";
import { BootstrapDisplay } from "../../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../../bootstrap/utilities/flex";
import { BootstrapHelpers } from "../../../bootstrap/utilities/helpers";
import { BootstrapPosition } from "../../../bootstrap/utilities/position";
import { BootstrapSpacing } from "../../../bootstrap/utilities/spacing";
import { BootstrapText } from "../../../bootstrap/utilities/text";
import { UserSessionManager } from "../../../session/UserSessionManager";
import { hasNumericKey } from "../../hasNumericKey";
import { createAvatarImage } from "../../user/createAvatarImage";
import { formatUserInfo } from "../../user/formatUserInfo";
import { createElement } from "../createElement";
import { createTextElement } from "../span/createTextElement";

export const createNameplate = (user, avatarHeight = "") => {
  const {
    nameTagText,
    avatarPathname,
    avatarAlt,
    isDisplayingStatus,
    id,
  } = formatUserInfo(user);

  const avatarImage = createAvatarImage({
    pathname: avatarPathname,
    alt: avatarAlt,
    height: avatarHeight,
  });
  const avatar = createAvatar({
    avatarImage,
    isDisplayingStatus,
    id,
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

const createAvatar = (params) => {
  const { avatarImage, isDisplayingStatus, id } = params;
  const container = createElement("div");
  container.append(avatarImage);
  if (!isDisplayingStatus) return container;

  const isOnline = getIsOnline(id);

  const badgeContainer = createElement("div");

  BootstrapPosition.setRelative(container);
  BootstrapPosition.setAbsolute(badgeContainer);
  BootstrapPosition.setStart(badgeContainer, 100);
  BootstrapPosition.setTop(badgeContainer, 100);
  BootstrapPosition.setTranslateMiddle(badgeContainer);

  const badge = createOnlineBadge(isOnline);

  badgeContainer.append(badge);
  container.append(badgeContainer);
  return container;
};

const getIsOnline = (id) =>
  UserSessionManager.getInstance().status.observe(
    (statusData) =>
      hasNumericKey(statusData, id) && statusData[id].isOnline,
  );

const createOnlineBadge = (isOnline) => {
  const onlineBadge = createElement("div");
  const setBgStyle = isOnline
    ? BootstrapBadge.setSuccess
    : BootstrapBadge.setSecondary;
  setBgStyle(onlineBadge);

  BootstrapBorders.setRoundedCircle(onlineBadge);
  BootstrapSpacing.setPadding(onlineBadge, 2);

  const hiddenText = createTextElement(
    isOnline ? "online" : "offline",
  );
  BootstrapHelpers.setVisuallyHidden(hiddenText);
  onlineBadge.append(hiddenText);
  return onlineBadge;
};
