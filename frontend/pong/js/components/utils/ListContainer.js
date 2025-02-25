import { Component } from "../../core/Component";
import { createDefaultListItem } from "../../utils/elements/li/createDefaultListItem";
import { createDefaultUnorderedList } from "../../utils/elements/ul/createDefaultUnorderedList";

export class ListContainer extends Component {
  #list;
  #subject;
  #appendNewItem;

  constructor(state = {}) {
    super({ ListItem: null, items: [], subject: null, ...state });
    const { ListItem, subject } = this._getState();

    this.#list = null;
    this.#subject = subject;
    this.#appendNewItem = ({ newItem }) => {
      const isScrolled = isAllScrolled(this.#list);
      this.#list.append(new ListItem({ item: newItem }));
      if (isScrolled) scrollAll(this.#list);
    };
  }

  _onConnect() {
    if (this.#subject) this.#subject.attach(this.#appendNewItem);
  }

  _onDisconnect() {
    if (this.#subject) this.#subject.detach(this.#appendNewItem);
  }

  _render() {
    const { ListItem, items } = this._getState();
    if (!ListItem) return;

    const listItemElements = items.map((item) =>
      createDefaultListItem([new ListItem({ item })]),
    );

    this.#list = createDefaultUnorderedList(listItemElements);
    this.append(this.#list);
  }
}

// https://developer.mozilla.org/en-US/docs/Web/API/Element/scrollHeight#determine_if_an_element_has_been_totally_scrolled
const isAllScrolled = (element) => {
  return (
    Math.abs(
      element.scrollHeight - element.clientHeight - element.scrollTop,
    ) <= 1
  );
};

const scrollAll = (element) => {
  element.scrollTop = element.scrollHeight;
};
