export class Component extends HTMLElement {
  _eventListeners;
  _state;

  constructor(state = {}) {
    super();
    this._eventListeners = [];
    this._state = state;
    this._init();
  }

  connectedCallback() {
    this._mount();
  }

  disconnectedCallback() {
    for (const { eventType, handler } of this._eventListeners) {
      this.removeEventListener(eventType, handler);
    }
    this._eventListeners = [];
  }

  _init() {}

  _getState(key) {
    return this._state[key];
  }

  _updateState(newState) {
    Object.assign(this._state, newState);
    this._mount();
  }

  _template() {
    return "";
  }

  _mount() {
    this.innerHTML = this._template();
    this._onMounted();
  }

  _onMounted() {}

  _attachListener(eventType, handler) {
    this.addEventListener(eventType, handler);
    this._eventListeners.push({ eventType, handler });
  }
}
