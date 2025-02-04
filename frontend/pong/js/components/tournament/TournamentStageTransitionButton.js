import { PongEvents } from "../../constants/PongEvents";
import { StyledButton } from "../../core/StyledButton";
import { TournamentEnums } from "../../enums/TournamentEnums";

export class TournamentStageTransitionButton extends StyledButton {
  #tournamentStage;
  #tournamentId;

  constructor(
    state = {},
    attributes = {},
    tournamentStage = TournamentEnums.Stage.ENTRANCE,
  ) {
    super(state, attributes);
    this.#tournamentStage = tournamentStage;
    this.#tournamentId = "<TOURNAMENT_ID>";
  }

  _onConnect() {
    this._attachEventListener("click", (event) => {
      event.preventDefault();
      const { target } = event;
      if (!(target instanceof HTMLButtonElement)) return;
      this.dispatchEvent(
        PongEvents.UPDATE_TOURNAMENT_STAGE.create(
          this.#tournamentStage,
          this.#tournamentId,
        ),
      );
    });
  }

  setTournamentId(tournamentId) {
    this.#tournamentId = tournamentId;
  }
}
