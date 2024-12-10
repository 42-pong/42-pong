import { View } from "../../core/View";

export class HomeView extends View {
  _template() {
    const currentPath = this._getPath();

    let str = `<h1>path: ${currentPath}</h1>`;
    const tabs = [
      { path: "/", title: "HOME" },
      { path: "/about", title: "ABOUT" },
      { path: "/not-in-routes", title: "NOT-IN-ROUTES" },
      { path: "/signout", title: "Sign Out" },
      { path: "/chat", title: "Chat Test" },
    ];
    for (const tab of tabs) {
      str += `<button class="btn" href="${tab.path}">${tab.title}</button>`;
    }
    return str;
  }

  _afterRender() {
    this._attachEventListener("click", (event) => {
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

// async loadStatus() {
//   let status = "404";
//   try {
//     const response = await fetch("http://localhost:8000/api/health");
//     const responseJson = await response.json();
//     status = responseJson.status;
//   } catch {
//     status = "KO";
//   }
//   this._updateState({ status });
// }
