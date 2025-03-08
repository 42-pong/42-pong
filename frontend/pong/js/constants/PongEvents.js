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

const UPDATE_USER_ID = {
  type: "update-user-id",
  create: (userId) =>
    createPongEvent(UPDATE_USER_ID.type, { userId }),
};

const TOGGLE_CHAT_GLOBAL = {
  type: "toggle-chat-global",
  create: () => createPongEvent(TOGGLE_CHAT_GLOBAL.type, {}),
};

const TOGGLE_CHAT_USER_SELECTION = {
  type: "toggle-chat-user",
  create: () => createPongEvent(TOGGLE_CHAT_USER_SELECTION.type, {}),
};

const START_MATCH = {
  type: "start-match",
  create: () => createPongEvent(START_MATCH.type, {}),
};

const END_MATCH = {
  type: "end-match",
  create: () => createPongEvent(END_MATCH.type, {}),
};

const TOGGLE_3D = {
  type: "toggle-3d",
  create: () => createPongEvent(TOGGLE_3D.type, {}),
};

const PATCH_DISPLAY_NAME = {
  type: "patch-display-name",
  create: () => createPongEvent(PATCH_DISPLAY_NAME.type, {}),
};

const PATCH_AVATAR = {
  type: "patch-avatar",
  create: () => createPongEvent(PATCH_AVATAR.type, {}),
};

const VERIFY_2FA = {
  type: "verify-2fa",
  create: (credentials) =>
    createPongEvent(VERIFY_2FA.type, { credentials }),
};

const VERIFY_TOTP = {
  type: "verify-totp",
  create: () => createPongEvent(VERIFY_TOTP.type, {}),
};

export const PongEvents = {
  UPDATE_ROUTER,
  UPDATE_TOURNAMENT_STAGE,
  UPDATE_USER_ID,
  TOGGLE_CHAT_GLOBAL,
  TOGGLE_CHAT_USER_SELECTION,
  START_MATCH,
  END_MATCH,
  TOGGLE_3D,
  PATCH_DISPLAY_NAME,
  PATCH_AVATAR,
  VERIFY_2FA,
  VERIFY_TOTP,
};
