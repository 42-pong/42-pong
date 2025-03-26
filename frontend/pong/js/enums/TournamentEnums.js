const Stage = {
  ENTRANCE: "ENTRANCE",
  PROGRESS: "PROGRESS",
};

const Status = {
  WAITING: "WAITING",
  ONGOING: "ONGOING",
  FINISHED: "FINISHED",
  CANCELED: "CANCELED",
};

const JoinType = {
  CREATE: "CREATE",
  RANDOM: "RANDOM",
  SELECTED: "SELECTED",
};

export const TournamentEnums = Object.freeze({
  Stage,
  Status,
  JoinType,
});
