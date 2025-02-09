import { BootstrapListGroup } from "../../../bootstrap/components/listGroup";
import { createElement } from "../createElement";

export const createDefaultListItem = (innerElements) => {
  const li = createElement("li");
  BootstrapListGroup.setListGroupItem(li);
  li.append(...innerElements);
  return li;
};
