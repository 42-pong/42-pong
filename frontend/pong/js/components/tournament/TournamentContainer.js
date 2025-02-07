import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { TournamentEnums } from "../../enums/TournamentEnums";
import { TournamentEntrance } from "./TournamentEntrance";
import { TournamentProgress } from "./TournamentProgress";

export class TournamentContainer extends Component {
  constructor(state) {
    super({
      stage: TournamentEnums.Stage.ENTRANCE,
      tournamentId: "",
      ...state,
    });
  }

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setJustifyContentCenter(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSizing.setWidth100(this);
    BootstrapSizing.setHeight100(this);
  }

  _onConnect() {
    this._attachEventListener(
      PongEvents.UPDATE_TOURNAMENT_STAGE.type,
      (event) => {
        const { stage, tournamentId } = event.detail;
        if (!(stage in TournamentEnums.Stage)) return;
        this._updateState({ stage, tournamentId });
      },
    );
  }

  _render() {
    const currentStageComponent = createCurrentStageComponent(this);
    this.appendChild(currentStageComponent);
  }
}

const createCurrentStageComponent = (tournamentContainer) => {
  const { stage, tournamentId } = tournamentContainer._getState();
  switch (stage) {
    case TournamentEnums.Stage.ENTRANCE:
      return new TournamentEntrance();
    case TournamentEnums.Stage.PROGRESS:
      return new TournamentProgress({
        tournamentId,
      });
    default:
      return new TournamentEntrance();
  }
};
