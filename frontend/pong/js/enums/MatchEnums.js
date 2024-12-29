const Stage = {
  INIT: "INIT",
  READY: "READY",
  PLAY: "PLAY",
  END: "END",
};

const Mode = {
  LOCAL: "local",
  REMOTE: "remote",
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

export const MatchEnums = Object.freeze({
  Stage,
  Mode,
  Team,
  Move,
});
