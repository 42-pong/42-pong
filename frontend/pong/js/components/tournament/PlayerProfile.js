import { getParticipations } from "../../api/participations/getParticipations";
import { BootstrapBadge } from "../../bootstrap/components/badge";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { BootstrapText } from "../../bootstrap/utilities/text";
import { Component } from "../../core/Component";
import { MatchEnums } from "../../enums/MatchEnums";
import { createElement } from "../../utils/elements/createElement";
import { createStartFlexBox } from "../../utils/elements/div/createFlexBox";
import { ParticipationProfile } from "./ParticipationProfile";

export class PlayerProfile extends Component {
  static #DEFAULT_HEIGHT = "max(15px, 3vh)";

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

const createScore = (scoreNum, matchResult) => {
  const score = createElement("div", { textContent: `${scoreNum}` });

  BootstrapText.setFontSize(score, 4);

  switch (matchResult) {
    case MatchEnums.Result.WIN:
      BootstrapBadge.setSuccess(score);
      break;
    case MatchEnums.Result.LOSE:
      BootstrapBadge.setDanger(score);
      break;
    case MatchEnums.Result.PENDING:
      BootstrapBadge.setSecondary(score);
      break;
    default:
      BootstrapBadge.setSecondary(score);
      break;
  }
  return score;
};
