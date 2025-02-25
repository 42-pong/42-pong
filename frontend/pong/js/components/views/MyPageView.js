import { AuthView } from "../../core/AuthView";

export class MyPageView extends AuthView {
  _render() {
    const title = document.createElement("h2");
    title.textContent = "My Page View";
    this.appendChild(title);
  }
}
