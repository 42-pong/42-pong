import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { View } from "../../core/View";
import { TournamentContainer } from "../tournament/TournamentContainer";

export class TournamentsView extends View {
  #tournamentContainer;

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setJustifyContentCenter(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSizing.setWidth100(this);
    BootstrapSizing.setViewportHeight100(this);
  }

  _onConnect() {
    // TODO: globalWebSocket Handler 登録

    this.#tournamentContainer = new TournamentContainer();
  }

  _onDisconnect() {
    // TODO: globalWebSocket Handler 登録解除
  }

  _render() {
    this.appendChild(this.#tournamentContainer);
  }
}
