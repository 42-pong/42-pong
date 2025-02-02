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

export const PongEvents = {
  UPDATE_ROUTER,
};
