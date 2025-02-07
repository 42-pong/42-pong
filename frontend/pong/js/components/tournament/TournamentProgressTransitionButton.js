import { PongEvents } from "../../constants/PongEvents";
import { StyledButton } from "../../core/StyledButton";
import { TournamentEnums } from "../../enums/TournamentEnums";

export class TournamentProgressTransitionButton extends StyledButton {
  #tournamentProgress;

  constructor(
    state = {},
    attributes = {},
    tournamentProgress = TournamentEnums.Progress.WAITING,
  ) {
    super(state, attributes);
    this.#tournamentProgress = tournamentProgress;
  }

  _onConnect() {
    this._attachEventListener("click", (event) => {
      event.preventDefault();
      const { target } = event;
      if (!(target instanceof HTMLButtonElement)) return;
      this.dispatchEvent(
        PongEvents.UPDATE_TOURNAMENT_PROGRESS.create(
          this.#tournamentProgress,
        ),
      );
    });
  }
}
