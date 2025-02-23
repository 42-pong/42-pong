import { BootstrapDisplay } from "../../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../../bootstrap/utilities/flex";
import { createElement } from "../createElement";

const createFlexBox = (...args) => {
  const container = createElement("div");
  BootstrapDisplay.setFlex(container);
  BootstrapFlex.setAlignItemsCenter(container);
  container.append(...args);
  return container;
};

const createDefaultFlexBox = (...args) => {
  const container = createFlexBox(...args);
  BootstrapFlex.setJustifyContentBetween(container);
  return container;
};

const createStartFlexBox = (...args) => {
  const container = createFlexBox(...args);
  BootstrapFlex.setJustifyContentStart(container);
  return container;
};

const createEndFlexBox = (...args) => {
  const container = createFlexBox(...args);
  BootstrapFlex.setJustifyContentEnd(container);
  return container;
};
export { createDefaultFlexBox, createStartFlexBox, createEndFlexBox };
