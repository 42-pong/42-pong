export class Component extends HTMLElement {
	_props;
	_state;

	constructor(props = {}, state = {}) {
		super();
		this._props = props;
		this._state = state;
		this._init();
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

	_afterRender() {}

	_render() {
		this.innerHTML = this._template();
		this._afterRender();
	}
}
