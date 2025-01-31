import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { Endpoints } from "../../constants/Endpoints";
import { View } from "../../core/View";
import { isOpenWebSocket } from "../../websocket";

export class HomeView extends View {
  
  #setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setJustifyContentCenter(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSizing.setWidth100(this);
    BootstrapSizing.setHeight100(this);
  }

  _onConnect() {
    this.#setStyle();
    Object.assign(this._state, {
      healthStatus: "...",
      webSocketBaseStatus: "...",
    });

    const getHealthStatus = async () => {
      let healthStatus;
      try {
        const res = await fetch(Endpoints.HEALTH.href);
        const json = await res.json();
        healthStatus = json.status;
      } catch (error) {
        console.error(error);
        healthStatus = "KO";
      }
      return healthStatus;
    };

    const getWebSocketBaseStatus = async () => {
      let isOpen;
      try {
        isOpen = await isOpenWebSocket();
      } catch (error) {
        isOpen = false;
      }
      return isOpen ? "OK" : "KO";
    };

    getHealthStatus().then((healthStatus) => {
      this._updateState({ healthStatus });
    });

    getWebSocketBaseStatus().then((webSocketBaseStatus) => {
      this._updateState({ webSocketBaseStatus });
    });
  }

  _render() {
    const title = document.createElement("h2");
    title.textContent = "Hello World";
    this.appendChild(title);

    const status = document.createElement("h3");
    status.textContent = `${Endpoints.HEALTH.pathname}: ${this._getState().healthStatus}`;
    this.appendChild(status);

    const wsStatus = document.createElement("h3");
    wsStatus.textContent = `${Endpoints.WEBSOCKET.pathname}: ${this._getState().webSocketBaseStatus}`;
    this.appendChild(wsStatus);
  }
}
