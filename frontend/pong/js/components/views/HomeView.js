import { Endpoints } from "../../Endpoints";
import { View } from "../../core/View";

export class HomeView extends View {
  _onConnect() {
    Object.assign(this._state, { healthStatus: "..." });

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

    getHealthStatus().then((healthStatus) => {
      this._updateState({ healthStatus });
    });
  }

  _render() {
    const title = document.createElement("h1");
    title.textContent = "Hello World";
    this.appendChild(title);

    const status = document.createElement("h2");
    status.textContent = `${Endpoints.HEALTH.pathname}: ${this._getState().healthStatus}`;
    this.appendChild(status);
  }
}
