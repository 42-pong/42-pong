import { getParticipations } from "../../api/participations/getParticipations";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Component } from "../../core/Component";
import { createStartFlexBox } from "../../utils/elements/div/createFlexBox";
import { ParticipationProfile } from "../tournament/ParticipationProfile";
import { createScore } from "./createScore";

export class PlayerProfile extends Component {
  static #DEFAULT_HEIGHT = "max(25px, 3vh)";

  _onConnect() {
    const { player } = this._getState();
    if (!player) return;
    const { tournamentId, userId } = player;

    getParticipations(tournamentId, userId).then(
      ({ participations, error }) => {
        if (error) return;
        const participation =
          participations.find(
            (participation) => participation.userId === userId,
          ) ?? null;
        if (!participation) return;
        this._updateState({ participation });
      },
    );
  }

  _render() {
    const { player, participation, height, matchResult } =
      this._getState();

    const score = createScore(player ? player.score : 0, matchResult);

    const participationProfile = new ParticipationProfile({
      participation,
      height: height ?? PlayerProfile.#DEFAULT_HEIGHT,
    });
    BootstrapSpacing.setMarginLeft(participationProfile, 4);

    const container = createStartFlexBox(score, participationProfile);
    this.append(container);
  }
}
