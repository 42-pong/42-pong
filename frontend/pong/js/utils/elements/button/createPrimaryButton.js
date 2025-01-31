import { BootstrapButtons } from "../../../bootstrap/components/buttons";
import { createElement } from "../createElement";

export const createPrimaryButton = (
  properties = {},
  attributes = {},
) => {
  const button = createElement("button", properties, attributes);
  BootstrapButtons.setButtonPrimary(button);
  return button;
};
