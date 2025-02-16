import { UserSession } from "./UserSession";

export const UserSessionManager = (() => {
  let instance = null;

  const getInstance = () => {
    if (!instance) instance = new UserSession();
    return instance;
  };

  return {
    getInstance,
    signIn: getInstance().signIn.bind(getInstance()),
    signOut: getInstance().signOut.bind(getInstance()),
    myInfoManager: getInstance().myInfoManager,
  };
})();
