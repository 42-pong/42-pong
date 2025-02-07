import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { Component } from "../../core/Component";
import { TournamentEnums } from "../../enums/TournamentEnums";
import { createElement } from "../../utils/elements/createElement";
import { TournamentProgressTransitionButton } from "./TournamentProgressTransitionButton";

export class TournamentOngoing extends Component {
  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setJustifyContentAround(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSizing.setWidth100(this);
    BootstrapSizing.setHeight100(this);
  }

  _render() {
    // TODO: タイトル要素を作成する関数でまとめる
    const title = createElement("h1", {
      textContent: "トーナメント進行中",
    });
    this.appendChild(title);

    // TODO: DELETE: 次の Progress に進むための一時的なもの
    const nextProgress = new TournamentProgressTransitionButton(
      { textContent: "次の PROGRESS (一時的)" },
      {},
      TournamentEnums.Progress.FINISHED,
    );
    nextProgress.setOutlineSecondary();
    BootstrapSizing.setWidth50(nextProgress);
    this.appendChild(nextProgress);
  }
}
