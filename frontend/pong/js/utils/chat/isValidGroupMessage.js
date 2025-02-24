export const isValidGroupMessage = (str) =>
  typeof str === "string" && str.length > 0 && str.length < 1000;
