import { View } from "../../core/View";

export class NotFoundView extends View {
  _render() {
    const title = document.createElement("h2");
    title.textContent = "Not Found View";
    this.appendChild(title);
  }
}
