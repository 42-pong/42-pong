const Category = {
  MATCH: "MATCH",
  TOURNAMENT: "TOURNAMENT",
};

const Tournament = {
  Type: {
    JOIN: "JOIN",
    LEAVE: "LEAVE",
    ASSIGNED: "ASSIGNED",
    RELOAD: "RELOAD",
  },
};

export const WebSocketEnums = Object.freeze({ Category, Tournament });
