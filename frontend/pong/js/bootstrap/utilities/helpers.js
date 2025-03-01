import { setClassNames } from "../../utils/elements/setClassNames";

const setVisuallyHidden = (element) => {
  return setClassNames(element, "visually-hidden");
};

export const BootstrapHelpers = {
  setVisuallyHidden,
};
