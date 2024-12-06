import { View } from "../../core/View";

export class HomeView extends View {
  // TODO
  async loadStatus() {
    let status = "404";
    try {
      const response = await fetch("http://localhost:8000/api/health");
      const responseJson = await response.json();
      status = responseJson.status;
    } catch {
      status = "KO";
    }
    this._updateState({ status });
  }

  _init() {
    const status = "???";
    this._updateState({ status });
    this.loadStatus();
  }

  _template() {
    const currentStatus = this._getState("status");
    const currentPath = this._getState("path");

    let str = `<h1>path: ${currentPath}</h1> <h2>Status: ${currentStatus}</h2>`;
    const tabs = [
      { path: "/", title: "HOME" },
      { path: "/about", title: "ABOUT" },
      { path: "/not-in-routes", title: "NOT-IN-ROUTES" },
      { path: "/signout", title: "Sign Out" },
    ];
    for (const tab of tabs) {
      str += `<button class="btn" href="${tab.path}">${tab.title}</button>`;
    }
    return str;
  }

  _onMounted() {
    const buttons = this.querySelectorAll(".btn");
    for (const button of buttons) {
      button.addEventListener("click", (event) => {
        const path = event.target.getAttribute("href");
        this.dispatchEvent(
          new CustomEvent("router", {
            detail: {
              path,
            },
            bubbles: true,
          }),
        );
      });
    }
  }
}
