import { setClassNames } from "../../utils/elements/setClassNames";

const setFluid = (containerElement) => {
  return setClassNames(containerElement, "container-fluid");
};

export const BootstrapContainers = {
  setFluid,
};
