import { TournamentEnums } from "../../enums/TournamentEnums";

export const convertStatus = (status) => {
  switch (status) {
    case "not_started":
      return TournamentEnums.Status.WAITING;
    case "on_going":
      return TournamentEnums.Status.ONGOING;
    case "completed":
      return TournamentEnums.Status.FINISHED;
    case "canceled":
      return TournamentEnums.Status.CANCELED;
    default:
      return TournamentEnums.Status.CANCELED;
  }
};
