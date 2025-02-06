import { createElement } from "../createElement";

export const createButton = (properties = {}, attributes = {}) => {
  return createElement("button", properties, attributes);
};
