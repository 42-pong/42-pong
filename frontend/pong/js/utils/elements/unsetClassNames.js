export const unsetClassNames = (element, ...classNames) => {
  if (element) element.classList.remove(...classNames);
  return element;
};
