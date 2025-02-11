const createPongEvent = (type, detail = {}) => {
  return new CustomEvent(type, { bubbles: true, detail });
};

const UPDATE_ROUTER = {
  type: "update-router",
  create: (path) => createPongEvent(UPDATE_ROUTER.type, { path }),
  trigger: (event) => {
    event.preventDefault();
    const { target } = event;
    if (!target?.pathname) return;
    target.dispatchEvent(UPDATE_ROUTER.create(target.pathname));
  },
};

const UPDATE_TOURNAMENT_STAGE = {
  type: "update-tournament-stage",
  create: (stage, tournamentId) =>
    createPongEvent(UPDATE_TOURNAMENT_STAGE.type, {
      stage,
      tournamentId,
    }),
};

const UPDATE_TOURNAMENT_PROGRESS = {
  type: "update-tournament-progress",
  create: (progress) =>
    createPongEvent(UPDATE_TOURNAMENT_PROGRESS.type, { progress }),
};

const UPDATE_USER_ID = {
  type: "update-user-id",
  create: (userId) =>
    createPongEvent(UPDATE_USER_ID.type, { userId }),
};

export const PongEvents = {
  UPDATE_ROUTER,
  UPDATE_TOURNAMENT_STAGE,
  UPDATE_TOURNAMENT_PROGRESS,
  UPDATE_USER_ID,
};
