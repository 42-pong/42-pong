export const createElement = (
  tagname,
  properties = {},
  attributes = {},
) => {
  const newElement = document.createElement(tagname);
  Object.assign(newElement, properties);
  for (const [key, value] of Object.entries(attributes)) {
    newElement.setAttribute(key, value);
  }
  return newElement;
};
