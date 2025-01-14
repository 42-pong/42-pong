const createPongEvent = (type, detail = {}) => {
  return new CustomEvent(type, { bubbles: true, detail });
};

const UPDATE_ROUTER = {
  type: "update-router",
  create: (path) => createPongEvent(UPDATE_ROUTER.type, { path }),
};

export const PongEvents = {
  UPDATE_ROUTER,
};
