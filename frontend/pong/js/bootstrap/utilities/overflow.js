import { setClassNames } from "../../utils/elements/setClassNames";

const setOverflowYAuto = (element) => {
  return setClassNames(element, "overflow-y-auto");
};

const setOverflowXHidden = (element) => {
  return setClassNames(element, "overflow-x-hidden");
};

export const BootstrapOverflow = {
  setOverflowYAuto,
  setOverflowXHidden,
};
