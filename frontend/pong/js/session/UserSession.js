import { DataManager } from "./DataManager";

export class UserSession {
  #myInfoManager;

  constructor() {
    this.#myInfoManager = new DataManager();
    this.init();
  }

  signIn(userData) {
    this.#myInfoManager.updateData({ ...userData, isSignedIn: true });
  }

  signOut() {
    this.init();
  }

  init() {
    this.#myInfoManager.init({ isSignedIn: false });
  }

  get myInfoManager() {
    return this.#myInfoManager;
  }
}
