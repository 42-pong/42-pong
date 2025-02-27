import { getTournament } from "../../api/tournaments/getTournament";
import { BootstrapBorders } from "../../bootstrap/utilities/borders";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { TournamentEnums } from "../../enums/TournamentEnums";
import { WebSocketEnums } from "../../enums/WebSocketEnums";
import { UserSessionManager } from "../../session/UserSessionManager";
import { isTournamentStateReload } from "../../utils/tournament/isTournamentStateReload";
import { TournamentFinished } from "./TournamentFinished";
import { TournamentOngoing } from "./TournamentOngoing";
import { TournamentWaiting } from "./TournamentWaiting";

export class TournamentStateContainer extends Component {
  #reloadTournamentState;

  constructor(state = {}) {
    super({ tournamentState: null, ...state });

    this.#reloadTournamentState = (payload) => {
      const {
        type,
        data: { event },
      } = payload;
      if (!isTournamentStateReload(type, event)) return;

      this.#reload();
    };
  }

  _setStyle() {
    BootstrapSizing.setWidth100(this);
    BootstrapBorders.setBorder(this);
    BootstrapBorders.setRounded(this);
  }

  _onConnect() {
    this.#reload();

    UserSessionManager.getInstance().webSocket.attachHandler(
      WebSocketEnums.Category.TOURNAMENT,
      this.#reloadTournamentState,
    );
  }

  _onDisconnect() {
    UserSessionManager.getInstance().webSocket.detachHandler(
      WebSocketEnums.Category.TOURNAMENT,
      this.#reloadTournamentState,
    );
  }

  _render() {
    const { tournamentState } = this._getState();
    if (!tournamentState) return;

    const { status } = tournamentState;
    const StatusComponent = getCurrentStatusComponent(status);
    const currentStatus = new StatusComponent({ tournamentState });
    this.append(currentStatus);
  }

  #reload() {
    const { tournamentId } = this._getState();
    getTournament(tournamentId).then(({ tournament, error }) => {
      if (error) {
        this.dispatchEvent(
          PongEvents.UPDATE_TOURNAMENT_STAGE.create(
            TournamentEnums.Stage.ENTRANCE,
            tournamentId,
          ),
        );
        return;
      }
      this._updateState({ tournamentState: tournament });
    });
  }
}

const getCurrentStatusComponent = (status) => {
  switch (status) {
    case TournamentEnums.Status.WAITING:
      return TournamentWaiting;
    case TournamentEnums.Status.ONGOING:
      return TournamentOngoing;
    case TournamentEnums.Status.FINISHED:
      return TournamentFinished;
    default:
      return TournamentWaiting;
  }
};
