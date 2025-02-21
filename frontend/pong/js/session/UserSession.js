import { ChatGlobal } from "../components/chat/ChatGlobal";
import { DataSubject } from "../core/DataSubject";
import { WebSocketWrapper } from "../websocket/WebSocketWrapper";

export class UserSession {
  #apps;
  #myInfo;
  #webSocket;
  #accessToken;

  constructor() {
    this.#apps = {};
    this.#myInfo = new DataSubject();
    this.#webSocket = new WebSocketWrapper();
  }

  signIn(userData) {
    this.#myInfo.updateData({ ...userData, isSignedIn: true });
    // TODO: WebSocket LOGIN
  }

  signOut() {
    this.#reset();
  }

  main(apps) {
    Object.assign(this.#apps, apps);
    this.#reset();
  }

  #reset() {
    const {
      appGlobal,
      updateWindowPath,
      displayMainLoading,
      displayMainError,
    } = this.#apps;

    clearGlobalFeatures(appGlobal);
    displayMainLoading();

    this.#init().then((isGood) => {
      if (isGood) {
        initGlobalFeatures(appGlobal);
        updateWindowPath();
      } else {
        displayMainError();
      }
    });
  }

  async #init() {
    this.#myInfo.init({ isSignedIn: false });
    this.#webSocket.close();

    const isConnected = await this.#webSocket.connect();
    return isConnected;
  }

  get myInfo() {
    return this.#myInfo;
  }

  get webSocket() {
    return this.#webSocket;
  }
}

const initGlobalFeatures = (globalRoot) => {
  const chatFeature = new ChatGlobal();

  globalRoot.append(chatFeature);
};

const clearGlobalFeatures = (globalRoot) => {
  globalRoot.replaceChildren();
};
