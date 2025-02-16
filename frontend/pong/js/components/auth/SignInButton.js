import { StyledButton } from "../../core/StyledButton";
import { UserSessionManager } from "../../session/UserSessionManager";

export class SignInButton extends StyledButton {
  constructor(state = {}, attributes = {}) {
    super(
      { textContent: "サインイン", ...state },
      { type: "button", ...attributes },
    );
  }

  _setStyle() {
    this.setOutlinePrimary();
    this.setSmall();
  }

  _onConnect() {
    this._attachEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();

      // TODO: DELETE: 一時的な対処なので確認が必要
      const mockUser = {
        id: 1,
        username: "user",
        email: "username1@example.com",
        displayName: "mock",
        avatar: "https://placehold.co/30",
      };
      UserSessionManager.signIn(mockUser, {});
    });
  }
}
