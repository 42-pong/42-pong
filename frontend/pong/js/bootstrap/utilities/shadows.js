import { setClassNames } from "../../utils/elements/setClassNames";

const setShadow = (element) => {
  return setClassNames(element, "shadow");
};

const setShadowSmall = (element) => {
  return setClassNames(element, "shadow-sm");
};

const setShadowLarge = (element) => {
  return setClassNames(element, "shadow-lg");
};

export const BootstrapShadows = {
  setShadow,
  setShadowSmall,
  setShadowLarge,
};
