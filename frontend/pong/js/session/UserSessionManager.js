import { UserSession } from "./UserSession";

export const UserSessionManager = (() => {
  let instance = null;

  const getInstance = () => {
    if (!instance) instance = new UserSession();
    return instance;
  };

  return {
    getInstance,
  };
})();
