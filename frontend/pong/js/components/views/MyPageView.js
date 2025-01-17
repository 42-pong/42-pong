import { View } from "../../core/View";

export class MyPageView extends View {
  _render() {
    const title = document.createElement("h2");
    title.textContent = "My Page View";
    this.appendChild(title);
  }
}
