import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { Component } from "../../core/Component";
import { TournamentScoreboard } from "./TournamentScoreboard";

export class TournamentOngoing extends Component {
  _setStyle() {
    BootstrapSizing.setWidth100(this);
    BootstrapSizing.setHeight100(this);
  }

  _render() {
    const { tournamentState } = this._getState();

    const scoreboard = new TournamentScoreboard({ tournamentState });
    BootstrapSizing.setWidth100(scoreboard);
    BootstrapSizing.setHeight100(scoreboard);
    this.append(scoreboard);
  }
}
