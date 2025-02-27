import { WebSocketEnums } from "../../enums/WebSocketEnums";

export const isPlayerReload = (type, event) =>
  type === WebSocketEnums.Tournament.Type.RELOAD &&
  event === WebSocketEnums.Tournament.ReloadEvent.PLAYER_CHANGE;
