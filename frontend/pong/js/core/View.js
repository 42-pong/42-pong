import { Component } from "./Component";

export class View extends Component {
  _updatePath(path) {
    if (this._getState("path") === path) return false;
    this._updateState({ path });
    return true;
  }
}
