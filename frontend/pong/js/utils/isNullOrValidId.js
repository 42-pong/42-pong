import { isValidId } from "./isValidId";

export const isNullOrValidId = (id) => id === null || isValidId(id);
