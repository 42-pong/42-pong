import { AuthView } from "../../core/AuthView";

export class DashboardView extends AuthView {
  _onConnect() {}

  _render() {
    this.append("dashboard");
  }
}
