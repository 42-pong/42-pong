import { DataSubject } from "./DataSubject";

export class UserSession {
  #myInfo;

  constructor() {
    this.#myInfo = new DataSubject();
    this.init();
  }

  signIn(userData) {
    this.#myInfo.updateData({ ...userData, isSignedIn: true });
  }

  signOut() {
    this.init();
  }

  init() {
    this.#myInfo.init({ isSignedIn: false });
  }

  get myInfo() {
    return this.#myInfo;
  }
}
