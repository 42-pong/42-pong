import { setClassNames } from "../../utils/elements/setClassNames";

const setButtonPrimary = (element) => {
  return setClassNames(element, "btn", "btn-primary");
};

export const BootstrapButtons = {
  setButtonPrimary,
};
