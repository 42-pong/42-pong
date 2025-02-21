import { PongEvents } from "../../constants/PongEvents";
import { StyledButton } from "../../core/StyledButton";
import { TournamentEnums } from "../../enums/TournamentEnums";

export class TournamentLeaveButton extends StyledButton {
  _onConnect() {
    this._attachEventListener("click", (event) => {
      event.preventDefault();
      const { target } = event;
      if (!(target instanceof HTMLButtonElement)) return;

      const { tournamentId } = this._getState();

      this.dispatchEvent(
        PongEvents.UPDATE_TOURNAMENT_STAGE.create(
          TournamentEnums.Stage.ENTRANCE,
          tournamentId,
        ),
      );
    });
  }
}
