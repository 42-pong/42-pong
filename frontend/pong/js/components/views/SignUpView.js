import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { AuthView } from "../../core/AuthView";
import { SignUpContainer } from "../auth/SignUpContainer";
export class SignUpView extends AuthView {
  #main;

  constructor(state = {}) {
    super({ authType: AuthView.Type.PROHIBITED, ...state });
  }

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setJustifyContentCenter(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSizing.setViewportHeight100(this);
    BootstrapSpacing.setPadding(this);

    BootstrapSizing.setWidth50(this.#main);
    BootstrapSizing.setHeight50(this.#main);
  }

  _onConnect() {
    this.#main = new SignUpContainer();
  }

  _render() {
    this.appendChild(this.#main);
  }
}
