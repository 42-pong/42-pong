import { View } from "../../core/View";

export class AboutView extends View {
  #title;

  _onConnect() {
    this.#title = document.createElement("h1");
    this.#title.textContent = "About World";
  }

  _render() {
    this.appendChild(this.#title);
  }
}
