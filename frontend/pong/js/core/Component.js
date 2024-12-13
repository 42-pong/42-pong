export class Component extends HTMLElement {
  _eventListeners;
  _state;

  constructor(state = {}) {
    super();
    this._eventListeners = [];
    this._state = state;
  }

  connectedCallback() {
    this._render();
  }

  disconnectedCallback() {
    for (const { eventType, handler } of this._eventListeners) {
      this.removeEventListener(eventType, handler);
    }
    this._eventListeners = [];
  }

  _getState() {
    return this._state;
  }

  _updateState(newState) {
    Object.assign(this._state, newState);
    this._render();
  }

  _template() {
    return "";
  }

  _render() {
    this.innerHTML = this._template();
    this._afterRender();
  }

  _afterRender() {}

  _attachEventListener(eventType, handler) {
    this.addEventListener(eventType, handler);
    this._eventListeners.push({ eventType, handler });
  }
}
