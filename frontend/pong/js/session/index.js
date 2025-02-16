import { UserSession } from "./UserSession";

let globalUserSession = null;

const initUserSession = () => {
  if (globalUserSession !== null) return;
  globalUserSession = new UserSession();
};

const getUserSession = () => {
  return globalUserSession;
};

export { initUserSession, getUserSession };
