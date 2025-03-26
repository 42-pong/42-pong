import { Endpoints } from "../../constants/Endpoints";

export const formatUserInfo = (user) =>
  user
    ? {
        nameTagText: `${user.displayName}#${user.username}`,
        avatarPathname: user.avatar,
        avatarAlt: `${user.displayName}#${user.username}'s avatar`,
        isDisplayingStatus: user.isDisplayingStatus ?? false,
        id: user.id,
      }
    : {
        nameTagText: "...",
        avatarPathname: Endpoints.USERS.defaultAvatar.href,
        avatarAlt: "placeholder",
        isDisplayingStatus: false,
        id: null,
      };
