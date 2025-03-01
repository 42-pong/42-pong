import { View } from "../../core/View";
import { SignUpContainer } from "../auth/SignUpContainer";
export class SignUpView extends View {
  #main;

  constructor(state = {}) {
    super({ ...state });
  }

  _onConnect() {
    this.#main = new SignUpContainer();
  }

  _render() {
    this.appendChild(this.#main);
  }
}
