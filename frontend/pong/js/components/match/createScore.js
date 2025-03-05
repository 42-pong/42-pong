import { BootstrapBadge } from "../../bootstrap/components/badge";
import { BootstrapText } from "../../bootstrap/utilities/text";
import { MatchEnums } from "../../enums/MatchEnums";
import { createElement } from "../../utils/elements/createElement";

export const createScore = (scoreNum, matchResult) => {
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
