export const sliceWithDefaults = (
  items,
  start,
  size,
  defaultElement = null,
) => {
  const sliced = items.slice(start, start + size);
  const defaults = Array(Math.max(0, size - sliced.length)).fill(
    defaultElement,
  );
  return [...sliced, ...defaults];
};
