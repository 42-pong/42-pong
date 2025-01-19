import { View } from "../../core/View";
import { LoginContainer } from "../auth/LoginContainer";

export class LoginView extends View {
  #main;

  _onConnect() {
    this.#main = new LoginContainer();
  }

  _render() {
    this.appendChild(this.#main);
  }
}
