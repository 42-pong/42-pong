export const isValidId = (id) =>
  typeof id === "number" && Number.isInteger(id) && id > 0;
