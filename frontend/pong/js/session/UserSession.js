import { getMyInfo } from "../api/users/getMyInfo";
import { ChatGlobal } from "../components/chat/ChatGlobal";
import { Paths } from "../constants/Paths";
import { PongEvents } from "../constants/PongEvents";
import { DataSubject } from "../core/DataSubject";
import { WebSocketEnums } from "../enums/WebSocketEnums";
import { initLang } from "../utils/i18n/lang";
import { WebSocketWrapper } from "../websocket/WebSocketWrapper";

export class UserSession {
  #apps;
  #myInfo;
  #status;
  #webSocket;

  #accessToken;

  constructor() {
    this.#apps = {};
    this.#myInfo = new DataSubject();
    this.#status = new DataSubject();
    const onError = this.onError.bind(this);
    this.#webSocket = new WebSocketWrapper({
      status: this.#status,
      onClose: onError,
      onError: onError,
    });
  }

  redirect(path = Paths.HOME) {
    const { app } = this.#apps;
    app.dispatchEvent(PongEvents.UPDATE_ROUTER.create(path));
  }

  async updateWindowPath() {
    const { updateWindowPath } = this.#apps;
    await updateWindowPath();
  }

  async main(apps) {
    Object.assign(this.#apps, apps);

    initLang();
    const isValid = await this.#reset();
    if (isValid) {
      await this.signIn();
      await this.updateWindowPath();
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
    } else {
      this.#clearTokens();
    }
    return isVerified;
  }

  async signOut() {
    this.#clearTokens();
    const isValid = await this.#reset();
    if (isValid) await this.updateWindowPath();
    return isValid;
  }

  async onError() {
    const { displayMainError } = this.#apps;
    displayMainError();
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

  getAccessToken() {
    return this.#accessToken;
  }

  getRefreshToken() {
    return sessionStorage.getItem("pong-refresh-token");
  }

  setAccessToken(access) {
    this.#accessToken = access;
  }

  setRefreshToken(refresh) {
    sessionStorage.setItem("pong-refresh-token", refresh);
  }

  #clearTokens() {
    this.#accessToken = "";
    sessionStorage.removeItem("pong-refresh-token");
  }
}

const initGlobalFeatures = (globalRoot) => {
  const chatFeature = new ChatGlobal();

  globalRoot.append(chatFeature);
};

const clearGlobalFeatures = (globalRoot) => {
  globalRoot.replaceChildren();
};
