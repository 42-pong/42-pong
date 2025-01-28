import { View } from "../../core/View";

export class UsersView extends View {
  _render() {
    const title = document.createElement("h2");
    title.textContent = "Users View";
    this.appendChild(title);
  }
}
