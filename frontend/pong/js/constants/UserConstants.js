const DisplayName = {
  MIN_LENGTH: 1,
  MAX_LENGTH: 15,
  VALID_REGEX: () =>
    new RegExp(
      `^[a-zA-Z0-9\-._~]{${DisplayName.MIN_LENGTH},${DisplayName.MAX_LENGTH}}$`,
    ),
};

export const UserConstants = Object.freeze({
  DisplayName,
});
