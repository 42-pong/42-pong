import { setClassNames } from "../../utils/elements/setClassNames";

const setListGroup = (element) => {
  return setClassNames(element, "list-group");
};

const setListGroupItem = (element) => {
  return setClassNames(element, "list-group-item");
};

export const BootstrapListGroup = {
  setListGroup,
  setListGroupItem,
};
