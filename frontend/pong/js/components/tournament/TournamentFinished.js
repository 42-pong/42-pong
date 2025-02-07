import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { Paths } from "../../constants/Paths";
import { Component } from "../../core/Component";
import { TournamentEnums } from "../../enums/TournamentEnums";
import { createElement } from "../../utils/elements/createElement";
import { LinkButton } from "../utils/LinkButton";
import { TournamentStageTransitionButton } from "./TournamentStageTransitionButton";

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

    this.#toTournamentEntrance = new TournamentStageTransitionButton(
      { textContent: "[トーナメント開始] に戻る" },
      {},
      TournamentEnums.Stage.ENTRANCE,
    );
  }

  _render() {
    // TODO: タイトル要素を作成する関数でまとめる
    const title = createElement("h1", {
      textContent: "トーナメント終了",
    });
    this.appendChild(title);

    this.appendChild(this.#toTournamentEntrance);
    this.appendChild(this.#toHome);
  }
}
