import { createJoin } from "./tournament/createJoin";
import { createLeave } from "./tournament/createLeave";

export const TournamentPayload = Object.freeze({
  createJoin,
  createLeave,
});
