import { BootstrapBorders } from "../../bootstrap/utilities/borders";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { Component } from "../../core/Component";
import { DataSubject } from "../../core/DataSubject";
import { createElement } from "../../utils/elements/createElement";

export class ObservableInput extends Component {
  #subject;
  #input;

  constructor(state = {}, attributes = {}) {
    super(state);
    this.#subject = new DataSubject();
    this.#input = createElement("input", {}, attributes);
  }

  get subject() {
    return this.#subject;
  }

  _setStyle() {
    BootstrapSizing.setWidth100(this.#input);
  }

  _onConnect() {
    this._attachEventListener("input", () => {
      this.#subject.updateData({ value: this.#input.value });
    });
    this.#subject.updateData({ value: this.#input.value });
  }

  _render() {
    this.append(this.#input);
  }

  setValue(value) {
    this.#input.value = value;
  }

  setError() {
    BootstrapBorders.setDanger(this.#input);
  }
}
