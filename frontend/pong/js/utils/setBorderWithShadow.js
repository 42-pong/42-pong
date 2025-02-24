import { BootstrapBorders } from "../bootstrap/utilities/borders";
import { BootstrapShadows } from "../bootstrap/utilities/shadows";

export const setBorderWithShadow = (element) => {
  BootstrapBorders.setBorder(element);
  BootstrapBorders.setRounded(element);
  BootstrapShadows.setShadow(element);
};
