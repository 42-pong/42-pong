import { View } from "../../core/View";
import { AboutView } from "./AboutView";

export class HomeView extends View {
  #title;
  #about;

  _onConnect() {
    this.#title = document.createElement("h1");

    this.#about = new AboutView();
    // this.#about = document.createElement("about-view");

    // initial 'isOpenAbout' value as 'false'
    this._getState().isOpenAbout = false;

    this._attachEventListener("click", (event) => {
      event.preventDefault();
      const currentIsOpenAbout = this._getState().isOpenAbout;
      const nextIsOpenAbout = !currentIsOpenAbout;

      this._updateState({ isOpenAbout: nextIsOpenAbout });
    });
  }

  _render() {
    switch (this._getPath()) {
      case "/":
        this.#title.textContent = "Hello World";
        break;
      case "/about":
        this.#title.textContent = "About World";
        break;
      case "/tmp":
        this.#title.textContent = "TMP-TMP";
        break;
      case "/users":
        this.#title.textContent = "USERS";
        break;
      default:
        this.#title.textContent = "DEFAULT";
        break;
    }

    this.appendChild(this.#title);

    const button = document.createElement("button");
    button.textContent = "Change to  '/About'";
    this.appendChild(button);

    if (this._getState().isOpenAbout) this.appendChild(this.#about);
  }
}
