import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { Component } from "../../core/Component";
import { TournamentEnums } from "../../enums/TournamentEnums";
import { createElement } from "../../utils/elements/createElement";
import { TournamentJoinButton } from "./TournamentJoinButton";
import { TournamentProgressTransitionButton } from "./TournamentProgressTransitionButton";

export class TournamentWaiting extends Component {
  #toTournamentEntrance;

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setJustifyContentAround(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSizing.setWidth100(this);
    BootstrapSizing.setHeight100(this);

    BootstrapSizing.setWidth50(this.#toTournamentEntrance);
    this.#toTournamentEntrance.setSecondary();
  }

  _onConnect() {
    this.#toTournamentEntrance = new TournamentJoinButton(
      { textContent: "戻る" },
      {},
      TournamentEnums.Stage.ENTRANCE,
    );
  }

  _render() {
    // TODO: タイトル要素を作成する関数でまとめる
    const title = createElement("h1", {
      textContent: "トーナメント開始の待機",
    });
    this.appendChild(title);

    // TODO: DELETE: 次の Progress に進むための一時的なもの
    const nextProgress = new TournamentProgressTransitionButton(
      { textContent: "次の PROGRESS (一時的)" },
      {},
      TournamentEnums.Progress.ONGOING,
    );
    nextProgress.setOutlineSecondary();
    BootstrapSizing.setWidth50(nextProgress);
    this.appendChild(nextProgress);

    this.appendChild(this.#toTournamentEntrance);
  }
}
