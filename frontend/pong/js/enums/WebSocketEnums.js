const Category = {
  MATCH: "MATCH",
  TOURNAMENT: "TOURNAMENT",
  CHAT: "CHAT",
  LOGIN: "LOGIN",
  STATUS: "STATUS",
};

const Tournament = {
  Type: {
    JOIN: "JOIN",
    LEAVE: "LEAVE",
    ASSIGNED: "ASSIGNED",
    RELOAD: "RELOAD",
  },
  ReloadEvent: {
    PLAYER_CHANGE: "PLAYER_CHANGE",
    TOURNAMENT_STATE_CHANGE: "TOURNAMENT_STATE_CHANGE",
  },
};

const Chat = {
  Type: {
    DM: "DM",
    GROUP_CHAT: "GROUP_CHAT",
    GROUP_ANNOUNCEMENT: "GROUP_ANNOUNCEMENT",
  },
};

export const WebSocketEnums = Object.freeze({
  Category,
  Tournament,
  Chat,
});
