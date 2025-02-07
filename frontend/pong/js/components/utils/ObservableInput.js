import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { Component } from "../../core/Component";
import { createElement } from "../../utils/elements/createElement";

// observer: (newValue, inputElement) => {...}
export class ObservableInput extends Component {
  #observers;
  #input;

  constructor(state = {}, attributes = {}) {
    super(state);
    this.#observers = new Set();
    this.#input = createElement("input", {}, attributes);
  }

  _setStyle() {
    BootstrapSizing.setWidth100(this.#input);
  }

  _onConnect() {
    this._attachEventListener("input", this.#notifyAll.bind(this));
  }

  _onDisconnect() {
    this.#observers = new Set();
    this.#input = null;
  }

  _render() {
    this.appendChild(this.#input);
  }

  attach(observer) {
    const isFunction = (f) => f instanceof Function;
    if (this.#observers.has(observer) || !isFunction(observer))
      return;
    this.#observers.add(observer);
    this.#notify(observer);
  }

  detach(observer) {
    if (!this.#observers.has(observer)) return;
    this.#observers.delete(observer);
  }

  #notify(observer) {
    observer(this.#input.value, this.#input);
  }

  #notifyAll() {
    for (const observer of this.#observers) {
      this.#notify(observer);
    }
  }
}
