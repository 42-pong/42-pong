import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { Paths } from "../../constants/Paths";
import { Component } from "../../core/Component";
import { createElement } from "../../utils/elements/createElement";
import { LinkButton } from "../utils/LinkButton";

export class TournamentFinished extends Component {
  #toTournamentEntrance;
  #toHome;

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setJustifyContentAround(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSizing.setWidth100(this);
    BootstrapSizing.setHeight100(this);

    BootstrapSizing.setWidth50(this.#toTournamentEntrance);
    this.#toTournamentEntrance.setPrimary();

    BootstrapSizing.setWidth50(this.#toHome);
    this.#toHome.setSecondary();
  }

  _onConnect() {
    this.#toHome = new LinkButton({
      textContent: "[ホーム] に戻る",
      pathname: Paths.HOME,
    });
  }

  _render() {
    // TODO: タイトル要素を作成する関数でまとめる
    const title = createElement("h1", {
      textContent: "トーナメント終了",
    });
    this.appendChild(title);

    this.appendChild(this.#toHome);
  }
}
