import { AuthView } from "../../core/AuthView";
import { LoginContainer } from "../auth/LoginContainer";

export class LoginView extends AuthView {
  #main;

  constructor(state = {}) {
    super({ authType: AuthView.Type.PROHIBITED, ...state });
  }

  _onConnect() {
    this.#main = new LoginContainer();
  }

  _render() {
    this.appendChild(this.#main);
  }
}
