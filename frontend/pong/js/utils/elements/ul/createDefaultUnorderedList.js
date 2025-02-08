import { BootstrapListGroup } from "../../../bootstrap/components/listGroup";
import { BootstrapOverflow } from "../../../bootstrap/utilities/overflow";
import { BootstrapSizing } from "../../../bootstrap/utilities/sizing";
import { createElement } from "../createElement";

export const createDefaultUnorderedList = (listItemElements) => {
  const ul = createElement("ul");
  BootstrapListGroup.setListGroup(ul);
  BootstrapSizing.setMaxHeight100(ul);
  BootstrapOverflow.setOverflowYAuto(ul);

  for (const li of listItemElements) {
    ul.append(li);
  }
  return ul;
};
