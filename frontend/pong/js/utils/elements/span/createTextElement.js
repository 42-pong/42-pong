import { BootstrapText } from "../../../bootstrap/utilities/text";
import { createElement } from "../createElement";

export const createTextElement = (
  textContent,
  fontSize,
  ...setStyles
) => {
  const textElement = createElement("span", { textContent });
  BootstrapText.setFontSize(textElement, fontSize);
  BootstrapText.setTextCenter(textElement);
  BootstrapText.setTextTruncate(textElement);
  for (const setStyle of setStyles) setStyle(textElement);
  return textElement;
};
