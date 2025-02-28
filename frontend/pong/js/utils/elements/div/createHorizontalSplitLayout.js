import { BootstrapDisplay } from "../../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../../bootstrap/utilities/sizing";
import { createElement } from "../createElement";

export const createHorizontalSplitLayout = (
  topElement,
  bottomElement,
) => {
  const container = createElement("div");
  BootstrapDisplay.setFlex(container);
  BootstrapFlex.setFlexColumn(container);
  BootstrapFlex.setAlignItemsCenter(container);
  BootstrapFlex.setJustifyContentAround(container);
  BootstrapSizing.setHeight100(container);

  container.append(topElement, bottomElement);
  return container;
};
