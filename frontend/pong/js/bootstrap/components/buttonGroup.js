import { setClassNames } from "../../utils/elements/setClassNames";

const setVertical = (element) => {
  return setClassNames(element, "btn-group-vertical");
};

export const BootstrapButtonGroup = {
  setVertical,
};
