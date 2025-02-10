import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { Paths } from "../../constants/Paths";
import { Component } from "../../core/Component";
import { createElement } from "../../utils/elements/createElement";
import { LinkButton } from "./LinkButton";

export class ErrorContainer extends Component {
  #toHome;

  constructor(state) {
    super({ message: "...", ...state });
  }

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSizing.setWidth100(this);
    BootstrapSizing.setHeight100(this);

    this.#toHome.setPrimary();
  }

  _onConnect() {
    this.#toHome = new LinkButton({
      textContent: "[ホーム] に戻る",
      pathname: Paths.HOME,
    });
  }

  _render() {
    const { message } = this._getState();

    const errorMessage = createElement("span", {
      textContent: `❗ Error: ${message}`,
    });

    this.append(errorMessage, this.#toHome);
  }
}
