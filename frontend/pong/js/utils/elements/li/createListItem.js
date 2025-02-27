import { BootstrapListGroup } from "../../../bootstrap/components/listGroup";
import { BootstrapSpacing } from "../../../bootstrap/utilities/spacing";
import { createElement } from "../createElement";

const createDefaultListItem = (innerElements) => {
  const li = createElement("li");
  BootstrapListGroup.setListGroupItem(li);
  li.append(...innerElements);
  return li;
};

const createInlineListItem = (innerElements) => {
  const li = createElement("li");
  BootstrapListGroup.setListInlineItem(li);
  BootstrapSpacing.setMargin(li, 3);
  li.append(...innerElements);
  return li;
};

export { createDefaultListItem, createInlineListItem };
