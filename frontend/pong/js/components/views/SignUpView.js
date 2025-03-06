import { AuthView } from "../../core/AuthView";
import { SignUpContainer } from "../auth/SignUpContainer";
export class SignUpView extends AuthView {
  #main;

  constructor(state = {}) {
    super({ authType: AuthView.Type.PROHIBITED, ...state });
  }

  _onConnect() {
    this.#main = new SignUpContainer();
  }

  _render() {
    this.appendChild(this.#main);
  }
}
