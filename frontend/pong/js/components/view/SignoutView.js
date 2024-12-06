import { View } from "../../core/View";

export class SignoutView extends View {
  _template() {
    const currentPath = this._getState("path");
    return `<h1>path: ${currentPath}</h1> <h2>Signout</h2>`;
  }
}
