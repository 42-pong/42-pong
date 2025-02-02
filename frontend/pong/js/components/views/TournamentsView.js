import { View } from "../../core/View";

export class TournamentsView extends View {
  _render() {
    const title = document.createElement("h2");
    title.textContent = "Tournaments View";
    this.appendChild(title);
  }
}
