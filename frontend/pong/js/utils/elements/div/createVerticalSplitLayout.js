import { BootstrapGrid } from "../../../bootstrap/layout/grid";
import { BootstrapDisplay } from "../../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../../bootstrap/utilities/sizing";
import { createElement } from "../createElement";

export const createVerticalSplitLayout = (
  leftElement,
  rightElement,
  leftColSize = 6,
  rightColSize = 6,
) => {
  const container = createElement("div");
  BootstrapDisplay.setFlex(container);
  BootstrapFlex.setAlignItemsCenter(container);
  BootstrapFlex.setJustifyContentAround(container);
  BootstrapSizing.setWidth100(container);

  BootstrapGrid.setCol(leftElement, leftColSize);
  BootstrapGrid.setCol(rightElement, rightColSize);
  container.append(leftElement, rightElement);
  return container;
};
