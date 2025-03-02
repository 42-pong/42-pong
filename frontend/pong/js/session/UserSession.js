import { getMyInfo } from "../api/users/getMyInfo";
import { ChatGlobal } from "../components/chat/ChatGlobal";
import { Paths } from "../constants/Paths";
import { PongEvents } from "../constants/PongEvents";
import { DataSubject } from "../core/DataSubject";
import { WebSocketEnums } from "../enums/WebSocketEnums";
import { WebSocketWrapper } from "../websocket/WebSocketWrapper";

export class UserSession {
  #apps;
  #myInfo;
  #status;
  #webSocket;

  // TODO: manage tokens
  #accessToken;
  #refreshToken;

  constructor() {
    this.#apps = {};
    this.#myInfo = new DataSubject();
    this.#status = new DataSubject();
    const signOut = this.signOut.bind(this);
    this.#webSocket = new WebSocketWrapper({
      status: this.#status,
      onClose: signOut,
      onError: signOut,
    });
  }

  redirect(path = Paths.HOME) {
    const { app } = this.#apps;
    app.dispatchEvent(PongEvents.UPDATE_ROUTER.create(path));
  }

  updateWindowPath() {
    const { updateWindowPath } = this.#apps;
    updateWindowPath();
  }

  async main(apps) {
    Object.assign(this.#apps, apps);

    const isValid = await this.#reset();
    if (isValid) {
      await this.signIn();
      this.updateWindowPath();
    }
    return isValid;
  }

  async #reset() {
    const { displayMainLoading, displayMainError } = this.#apps;

    displayMainLoading();

    const isValid = await this.#init();
    if (!isValid) displayMainError();
    return isValid;
  }

  async #init() {
    const { appGlobal } = this.#apps;
    clearGlobalFeatures(appGlobal);
    this.#initTokens();
    this.#myInfo.init({ isSignedIn: false });
    this.#status.init();
    this.#webSocket.close();

    const isConnected = await this.#webSocket.connect();
    return isConnected;
  }

  async signIn(authData = null) {
    if (authData) {
      const { access, refresh } = authData;
      this.setAccessToken(access);
      this.setRefreshToken(refresh);
    }
    const isVerified = await this.verifyAuth();
    if (isVerified) {
      const id = this.myInfo.observe(({ id }) => id);
      this.webSocket.send(WebSocketEnums.Category.LOGIN, {
        user_id: id,
      });
      // initGlobalFeatures(appGlobal);
    }
    return isVerified;
  }

  async signOut() {
    const isValid = await this.#reset();
    if (isValid) this.updateWindowPath();
    return isValid;
  }

  async verifyAuth() {
    const { myInfo, error } = await getMyInfo();
    if (error) return false;
    this.#myInfo.updateData({ ...myInfo, isSignedIn: true });
    return true;
  }

  async assertAuth() {
    const isVerified = await this.verifyAuth();
    if (!isVerified && (await this.#reset()))
      this.redirect(Paths.LOGIN);
    return isVerified;
  }

  async assertNoAuth() {
    const isVerified = await this.verifyAuth();
    if (isVerified) this.redirect(Paths.HOME);
    return isVerified;
  }

  get myInfo() {
    return this.#myInfo;
  }

  get status() {
    return this.#status;
  }

  get webSocket() {
    return this.#webSocket;
  }

  // TODO: manage tokens
  getAccessToken() {
    return this.#accessToken;
  }

  getRefreshToken() {
    console.log("get refresh token");
    // return this.#refreshToken;
  }

  setAccessToken(access) {
    this.#accessToken = access;
  }

  setRefreshToken(refresh) {
    console.log("set refresh token");
    // this.#refreshToken = refresh;
  }

  #initTokens() {
    this.#accessToken = "";
    this.#refreshToken = "";
  }
}

const initGlobalFeatures = (globalRoot) => {
  const chatFeature = new ChatGlobal();

  globalRoot.append(chatFeature);
};

const clearGlobalFeatures = (globalRoot) => {
  globalRoot.replaceChildren();
};
