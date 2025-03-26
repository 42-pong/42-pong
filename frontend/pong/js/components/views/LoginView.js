import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { PongEvents } from "../../constants/PongEvents";
import { AuthView } from "../../core/AuthView";
import { LoginContainer } from "../auth/LoginContainer";
import { Verify2faContainer } from "../auth/Verify2faContainer";

export class LoginView extends AuthView {
  constructor(state = {}) {
    super({
      authType: AuthView.Type.PROHIBITED,
      is2faRunning: false,
      ...state,
    });
  }

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setJustifyContentCenter(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSizing.setViewportHeight100(this);
    BootstrapSpacing.setPadding(this);
  }

  _onConnect() {
    this._attachEventListener(PongEvents.VERIFY_2FA.type, (event) => {
      event.preventDefault();
      const {
        detail: { credentials },
      } = event;
      this._updateState({
        is2faRunning: true,
        credentials,
      });
    });
  }

  _render() {
    const { is2faRunning, credentials } = this._getState();
    const main = is2faRunning
      ? new Verify2faContainer({ credentials })
      : new LoginContainer();
    BootstrapSizing.setWidth50(main);
    BootstrapSizing.setHeight50(main);
    this.append(main);
  }
}
