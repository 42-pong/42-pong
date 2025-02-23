import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { View } from "../../core/View";
import { setBorderWithShadow } from "../../utils/setBorderWithShadow";
import { GameStartPanel } from "../game/GameStartPanel";

export class HomeView extends View {
  #gameStartPanel;

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setJustifyContentCenter(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSizing.setWidth100(this);
    BootstrapSizing.setHeight100(this);

    setBorderWithShadow(this);
  }

  _onConnect() {
    this.#gameStartPanel = new GameStartPanel();
  }

  _render() {
    this.appendChild(this.#gameStartPanel);
  }
}
