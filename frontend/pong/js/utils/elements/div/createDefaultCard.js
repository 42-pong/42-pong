import { BootstrapCard } from "../../../bootstrap/components/card";
import { BootstrapFlex } from "../../../bootstrap/utilities/flex";
import { createElement } from "../createElement";

export const createDefaultCard = (elementsObject) => {
  const card = createElement("div");
  const cardBody = createElement("div");

  BootstrapCard.setCard(card);
  BootstrapCard.setCardBody(cardBody);
  BootstrapFlex.setAlignItemsCenter(cardBody);

  appendCardRelatedElements(card, cardBody, elementsObject);

  return card;
};

const appendCardRelatedElements = (
  card,
  cardBody,
  elementsObject,
) => {
  const { title, subtitle, text, others } = elementsObject;
  const bodyElements = [];

  if (title) {
    BootstrapCard.setCardTitle(title);
    bodyElements.push(title);
  }
  if (subtitle) {
    BootstrapCard.setCardSubtitle(subtitle);
    bodyElements.push(subtitle);
  }
  if (text) {
    BootstrapCard.setCardText(text);
    bodyElements.push(text);
  }
  if (others) bodyElements.push(...others);

  cardBody.append(...bodyElements);
  card.append(cardBody);
};
