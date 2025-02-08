import { setClassNames } from "../../utils/elements/setClassNames";

const setCard = (element) => {
  return setClassNames(element, "card");
};

const setCardBody = (element) => {
  return setClassNames(element, "card-body");
};

const setCardTitle = (element) => {
  return setClassNames(element, "card-title");
};

const setCardSubtitle = (element) => {
  return setClassNames(element, "card-subtitle");
};

const setCardText = (element) => {
  return setClassNames(element, "card-text");
};

export const BootstrapCard = {
  setCard,
  setCardBody,
  setCardTitle,
  setCardSubtitle,
  setCardText,
};
