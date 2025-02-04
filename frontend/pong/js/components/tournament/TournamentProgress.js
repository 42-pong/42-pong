import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { TournamentEnums } from "../../enums/TournamentEnums";
import { createElement } from "../../utils/elements/createElement";
import { TournamentFinished } from "./TournamentFinished";
import { TournamentOngoing } from "./TournamentOngoing";
import { TournamentWaiting } from "./TournamentWaiting";

export class TournamentProgress extends Component {
  constructor(state) {
    super({
      players: [],
      progress: TournamentEnums.Progress.WAITING,
      ...state,
    });
  }

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setJustifyContentCenter(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSizing.setWidth75(this);
    BootstrapSizing.setHeight75(this);
  }

  _onConnect() {
    // TODO: fetch players

    // TODO: attach websocket PROGRESS handling

    this._attachEventListener(
      PongEvents.UPDATE_TOURNAMENT_PROGRESS.type,
      (event) => {
        const { progress } = event.detail;
        if (!(progress in TournamentEnums.Progress)) return;
        this._updateState({ progress });
      },
    );
  }

  _onDisconnect() {
    // TODO: detach websocket PROGRESS handling
  }

  _render() {
    const { tournamentId } = this._getState();
    // TODO: タイトル要素を作成する関数でまとめる
    const title = createElement("h1");
    title.textContent = `🏓 #${tournamentId}`;
    this.appendChild(title);

    const currentProgressComponent =
      createCurrentProgressComponent(this);
    this.appendChild(currentProgressComponent);
  }
}

const createCurrentProgressComponent = (tournamentProgress) => {
  const { progress, tournamentId, players } =
    tournamentProgress._getState();
  switch (progress) {
    case TournamentEnums.Progress.WAITING:
      return new TournamentWaiting({
        tournamentId,
        players,
      });
    case TournamentEnums.Progress.ONGOING:
      return new TournamentOngoing({
        tournamentId,
        players,
      });
    case TournamentEnums.Progress.FINISHED:
      return new TournamentFinished();
    default:
      return new TournamentWaiting();
  }
};
