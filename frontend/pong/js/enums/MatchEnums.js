const Stage = {
  INIT: "INIT",
  READY: "READY",
  PLAY: "PLAY",
  END: "END",
};

const Mode = {
  LOCAL: "LOCAL",
  REMOTE: "REMOTE",
};

const Team = {
  ONE: "1",
  TWO: "2",
  EMPTY: "",
};

const Move = {
  UP: "UP",
  DOWN: "DOWN",
};

const Result = {
  WIN: "WIN",
  LOSE: "LOSE",
  PENDING: "PENDING",
};

export const MatchEnums = Object.freeze({
  Stage,
  Mode,
  Team,
  Move,
  Result,
});
