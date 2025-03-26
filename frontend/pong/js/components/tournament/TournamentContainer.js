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
        event.preventDefault();
        const { stage, tournamentId } = event.detail;
        if (!(stage in TournamentEnums.Stage)) return;
        this._updateState({ stage, tournamentId });
      },
    );
  }

  _render() {
    const { stage, tournamentId } = this._getState();
    const currentStageComponent = createCurrentStageComponent(
      stage,
      tournamentId,
    );
    this.append(currentStageComponent);
  }
}

const createCurrentStageComponent = (stage, tournamentId) => {
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
