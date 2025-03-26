export class Component extends HTMLElement {
  _eventListeners;
  _state;

  constructor(state = {}) {
    super();
    this._eventListeners = [];
    this._state = state;
  }

  _getState() {
    return this._state;
  }
  _updateState(newState) {
    Object.assign(this._state, newState);
    this._update();
  }

  _preConnect() {}
  _onConnect() {}
  _onDisconnect() {}
  _render() {}
  _cleanup() {
    this.replaceChildren();
  }
  _setStyle() {}

  connectedCallback() {
    this._preConnect();
    this._onConnect();
    this._setStyle();
    this._render();
  }

  disconnectedCallback() {
    this._cleanup();
    this._onDisconnect();
    this._detachAllEventListeners();
  }

  _update() {
    this._cleanup();
    this._render();
  }

  _attachEventListener(eventType, handler) {
    this.addEventListener(eventType, handler);
    this._eventListeners.push({ eventType, handler });
  }

  _detachAllEventListeners() {
    for (const { eventType, handler } of this._eventListeners) {
      this.removeEventListener(eventType, handler);
    }
    this._eventListeners = [];
  }
}
