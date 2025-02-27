import { BootstrapBadge } from "../../bootstrap/components/badge";
import { TournamentEnums } from "../../enums/TournamentEnums";
import { createElement } from "../elements/createElement";

export const createStatusBadge = (status) => {
  const badge = createElement("span", { textContent: status });
  styleBadge(badge, status);
  return badge;
};

const styleBadge = (badge, status) => {
  switch (status) {
    case TournamentEnums.Status.WAITING:
      BootstrapBadge.setSecondary(badge);
      break;
    case TournamentEnums.Status.ONGOING:
      BootstrapBadge.setPrimary(badge);
      break;
    case TournamentEnums.Status.FINISHED:
      BootstrapBadge.setWarning(badge);
      break;
    case TournamentEnums.Status.CANCELED:
      BootstrapBadge.setDark(badge);
      break;
    default:
      BootstrapBadge.setSecondary(badge);
      break;
  }
};
