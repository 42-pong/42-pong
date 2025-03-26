import { Component } from "./Component";

export class View extends Component {
  constructor(state = {}) {
    super({ path: View._defaultPath, ...state });
  }

  _getPath() {
    return this._getState().path;
  }

  _updatePath(path) {
    if (this._getPath() === path) return false;
    this._updateState({ path });
    return true;
  }

  static get _defaultPath() {
    return "/";
  }
}
