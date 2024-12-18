import { View } from "../../core/View";
//import { AboutView } from "./AboutView";
import { LoginView } from "./LoginView";

export class HomeView extends View {
  #title;
  #about;
  #login;

  _onConnect() {
    this.#title = document.createElement("h1");

    //this.#about = new AboutView();
    this.#login = new LoginView();

    this.#about = document.createElement("about-view");

    // initial 'isOpenAbout' value as 'false'
    this._getState().isOpenAbout = false;
    this._getState().isOpenLogin = false;
  }

  _render() {
    switch (this._getPath()) {
      case "/":
        this.#title.textContent = "Hello World";
        break;
      case "/about":
        this.#title.textContent = "About";
        break;
      case "/login":
        this.#title.textContent = "Login";
        this.appendChild(this.#login);
        break;
      case "/users":
        this.#title.textContent = "USERS";
        break;
      default:
        this.#title.textContent = "DEFAULT";
        break;
    }

    this.appendChild(this.#title);

    const aboutButton = document.createElement("button");
    aboutButton.textContent = "Change to  '/about'";
    aboutButton.addEventListener("click", (event) => {
      event.preventDefault();
      this._updateState({
        isOpenAbout: !this._getState().isOpenAbout,
      });
      this._updatePath("/about");
    });
    this.appendChild(aboutButton);

    const loginButton = document.createElement("button");
    loginButton.textContent = "Change to '/login'";
    loginButton.addEventListener("click", (event) => {
      event.preventDefault();
      console.log("login");
      // this._updateState({ isOpenLogin: !this._getState().isOpenLogin});
      // this._updatePath("/login");
      this.dispatchEvent(
        new CustomEvent("router", {
          bubbles: true,
          detail: { path: "/login-test" },
        }),
      );
    });
    this.appendChild(loginButton);

    if (this._getState().isOpenAbout) this.appendChild(this.#about);
  }
}
