import { Paths } from "../constants/Paths";
import { UserSessionManager } from "../session/UserSessionManager";

export const handleAuthPath = async () => {
  if (window.location.pathname !== Paths.OAUTH) return false;

  const params = new URLSearchParams(window.location.search);
  const access = params.get("access");
  const refresh = params.get("refresh");

  window.history.replaceState(null, "", "/");

  const isVerified =
    access &&
    refresh &&
    (await UserSessionManager.getInstance().signIn({
      access,
      refresh,
    }));
  const nextPath = isVerified ? Paths.HOME : Paths.LOGIN;
  UserSessionManager.getInstance().redirect(nextPath);

  return true;
};
