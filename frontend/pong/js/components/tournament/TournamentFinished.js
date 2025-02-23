import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Paths } from "../../constants/Paths";
import { Component } from "../../core/Component";
import { createDefaultFlexBox } from "../../utils/elements/div/createFlexBox";
import { createHorizontalSplitLayout } from "../../utils/elements/div/createHorizontalSplitLayout";
import { setHeight } from "../../utils/elements/style/setHeight";
import { LinkButton } from "../utils/LinkButton";
import { TournamentLeaveButton } from "./TournamentLeaveButton";
import { TournamentScoreboard } from "./TournamentScoreboard";

export class TournamentFinished extends Component {
  #buttons;

  _setStyle() {
    BootstrapSizing.setWidth100(this);
    BootstrapSizing.setHeight100(this);

    BootstrapSpacing.setPadding(this.#buttons, 4);
  }

  _onConnect() {
    const {
      tournamentState: { tournamentId },
    } = this._getState();
    this.#buttons = createReturningButtons(tournamentId);
  }

  _render() {
    const { tournamentState } = this._getState();

    const scoreboard = new TournamentScoreboard({ tournamentState });
    BootstrapSizing.setWidth100(scoreboard);
    setHeight(scoreboard, "80%");
    setHeight(this.#buttons, "20%");

    const split = createHorizontalSplitLayout(
      scoreboard,
      this.#buttons,
    );
    this.append(split);
  }
}

const createReturningButtons = (tournamentId) => {
  const backToTournamentEntrance = new TournamentLeaveButton({
    textContent: "もう一度",
    tournamentId,
  });
  backToTournamentEntrance.setPrimary();
  BootstrapSpacing.setMargin(backToTournamentEntrance, 3);

  const backToHome = new LinkButton({
    textContent: "ホームに戻る",
    pathname: Paths.HOME,
  });
  backToHome.setOutlinePrimary();
  BootstrapSpacing.setMargin(backToHome, 3);

  return createDefaultFlexBox(
    createDefaultFlexBox(backToTournamentEntrance),
    createDefaultFlexBox(backToHome),
  );
};
