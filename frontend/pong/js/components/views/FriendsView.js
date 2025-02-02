import { View } from "../../core/View";

export class FriendsView extends View {
  _render() {
    const title = document.createElement("h2");
    title.textContent = "Friends View";
    this.appendChild(title);
  }
}
