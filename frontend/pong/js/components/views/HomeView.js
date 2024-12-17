import { View } from "../../core/View";

export class HomeView extends View {
  _render() {
    const title = document.createElement("h1");
    title.textContent = "Hello World";
    this.appendChild(title);
  }
}
