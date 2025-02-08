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
  if (title) {
    BootstrapCard.setCardTitle(title);
    cardBody.append(title);
  }
  if (subtitle) {
    BootstrapCard.setCardSubtitle(subtitle);
    cardBody.append(subtitle);
  }
  if (text) {
    BootstrapCard.setCardText(text);
    cardBody.append(text);
  }
  if (others) cardBody.append(...others);
  card.append(cardBody);
};
