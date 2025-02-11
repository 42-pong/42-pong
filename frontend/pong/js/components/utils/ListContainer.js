import { Component } from "../../core/Component";
import { createDefaultListItem } from "../../utils/elements/li/createDefaultListItem";
import { createDefaultUnorderedList } from "../../utils/elements/ul/createDefaultUnorderedList";

export class ListContainer extends Component {
  constructor(state = {}) {
    super({ ListItem: null, items: [], ...state });
  }

  _render() {
    const { ListItem, items } = this._getState();
    if (!ListItem) return;

    const listItemElements = items.map((item) =>
      createDefaultListItem([new ListItem({ item })]),
    );

    const listElement = createDefaultUnorderedList(listItemElements);

    this.append(listElement);
  }
}
