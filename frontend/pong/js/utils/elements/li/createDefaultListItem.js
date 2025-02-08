import { BootstrapListGroup } from "../../../bootstrap/components/listGroup";
import { createElement } from "../createElement";

export const createDefaultListItem = (innerElements) => {
  const li = createElement("li");
  BootstrapListGroup.setListGroupItem(li);
  for (const element of innerElements) {
    li.append(element);
  }
  return li;
};
