import { WebSocketEnums } from "../../enums/WebSocketEnums";

export const isTournamentStateReload = (type, event) =>
  type === WebSocketEnums.Tournament.Type.RELOAD &&
  event ===
    WebSocketEnums.Tournament.ReloadEvent.TOURNAMENT_STATE_CHANGE;
