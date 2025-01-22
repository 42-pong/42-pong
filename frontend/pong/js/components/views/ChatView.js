import { View } from "../../core/View";

export class ChatView extends View {
  _render() {
    const title = document.createElement("h2");
    title.textContent = "Chat View";
    this.appendChild(title);
  }
}
