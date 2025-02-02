export const setClassNames = (element, ...classNames) => {
  if (element) element.classList.add(...classNames);
  return element;
};
