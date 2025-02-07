import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Paths } from "../../constants/Paths";
import { Component } from "../../core/Component";
import { TournamentEnums } from "../../enums/TournamentEnums";
import { createElement } from "../../utils/elements/createElement";
import { LinkButton } from "../utils/LinkButton";
import { TournamentStageTransitionButton } from "./TournamentStageTransitionButton";
import { TournamentStageTransitionButtonWithInput } from "./TournamentStageTransitionButtonWithInput";

export class TournamentEntrance extends Component {
  #entranceButtons;
  #toHome;

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setJustifyContentAround(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSizing.setWidth75(this);
    BootstrapSizing.setHeight75(this);

    BootstrapDisplay.setGrid(this.#entranceButtons);
    BootstrapSizing.setWidth50(this.#entranceButtons);
    BootstrapSpacing.setGap(this.#entranceButtons);

    BootstrapSizing.setWidth50(this.#toHome);
    this.#toHome.setSecondary();
  }

  _onConnect() {
    this.#entranceButtons = createTournamentEntranceButtons();
    this.#toHome = new LinkButton({
      textContent: "戻る",
      pathname: Paths.HOME,
    });
  }

  _onDisconnect() {}

  _render() {
    // TODO: タイトル要素を作成する関数でまとめる
    const title = createElement("h1", {
      textContent: "🏓 トーナメント開始",
    });
    this.appendChild(title);

    this.appendChild(this.#entranceButtons);
    this.appendChild(this.#toHome);
  }
}

const createTournamentEntranceButtons = () => {
  const joinRandom = new TournamentStageTransitionButton(
    { textContent: "ランダム参加" },
    {},
    TournamentEnums.Stage.PROGRESS,
  );

  const joinWithCreation = new TournamentStageTransitionButton(
    { textContent: "トーナメント作成" },
    {},
    TournamentEnums.Stage.PROGRESS,
  );

  const joinWithInput = new TournamentStageTransitionButtonWithInput(
    {},
    {
      type: "text",
      placeholder: "トーナメント ID",
      value: "",
    },
    { textContent: "参加" },
    {},
    TournamentEnums.Stage.PROGRESS,
  );

  joinRandom.setPrimary();
  joinWithCreation.setOutlinePrimary();
  joinWithInput.setOutlinePrimary();

  const container = createElement("div");
  container.appendChild(joinRandom);
  container.appendChild(joinWithCreation);
  container.appendChild(joinWithInput);
  return container;
};
