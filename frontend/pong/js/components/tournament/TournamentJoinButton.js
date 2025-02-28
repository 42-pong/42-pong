import { StyledButton } from "../../core/StyledButton";
import { WebSocketEnums } from "../../enums/WebSocketEnums";
import { UserSessionManager } from "../../session/UserSessionManager";
import { TournamentPayload } from "../../websocket/payload/TournamentPayload";

export class TournamentJoinButton extends StyledButton {
  _onConnect() {
    this._attachEventListener("click", (event) => {
      event.preventDefault();
      const { target } = event;
      if (!(target instanceof HTMLButtonElement)) return;

      const { joinType, getDisplayName, getTournamentId } =
        this._getState();

      const { displayName, tournamentId, isError } = getParams(
        getDisplayName,
        getTournamentId,
      );
      if (isError) return;

      UserSessionManager.getInstance().webSocket.send(
        WebSocketEnums.Category.TOURNAMENT,
        TournamentPayload.createJoin({
          joinType,
          tournamentId,
          displayName,
        }),
      );
    });
  }
}

const getParams = (getDisplayName, getTournamentId) => {
  let isError = false;

  const { displayName, error } = getDisplayName();
  if (error) isError = true;

  let tournamentId = null;
  if (getTournamentId) {
    const { id, error } = getTournamentId();
    tournamentId = id;
    if (error) isError = true;
  }

  return { displayName, tournamentId, isError };
};
