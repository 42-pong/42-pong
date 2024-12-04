export class Component extends HTMLElement {
  _name;
  _props;
  _state;

  constructor() {
    super();
    this._name = "component-name";
    this._props = {};
    this._state = {};
    this._init();
    console.log(`${this._name}: constructor`);
  }
  connectedCallback() {
    this._render();
    console.log(`${this._name}: connectedCallback`);
  }
  disconnectedCallback() {
    console.log(`${this._name}: disconnectedCallback`);
  }

  _init() {}

  _getProps(key) {
    return this._props[key];
  }

  _getState(key) {
    return this._state[key];
  }
  _setState(newState) {
    Object.assign(this._state, newState);
    this._render();
  }

  _template() {
    return "<div></div>";
  }

  _render() {
    this.innerHTML = this._template();
  }
}
