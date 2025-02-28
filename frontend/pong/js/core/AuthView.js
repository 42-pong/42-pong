import { UserSessionManager } from "../session/UserSessionManager";
import { View } from "./View";

export class AuthView extends View {
  static Type = Object.freeze({
    REQUIRED: "REQUIRED",
    PROHIBITED: "PROHIBITED",
  });

  constructor(state = {}) {
    super({ authType: AuthView.Type.REQUIRED, ...state });
  }

  _preConnect() {
    const { authType } = this._getState();
    switch (authType) {
      case AuthView.Type.REQUIRED:
        UserSessionManager.getInstance().assertAuth();
        break;
      case AuthView.Type.PROHIBITED:
        UserSessionManager.getInstance().assertNoAuth();
        break;
      default:
        break;
    }
  }
}
