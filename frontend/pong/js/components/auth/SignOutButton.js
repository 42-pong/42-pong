import { StyledButton } from "../../core/StyledButton";
import { UserSessionManager } from "../../session/UserSessionManager";
import { getTextContent } from "../../utils/i18n/lang";

export class SignOutButton extends StyledButton {
  constructor(state = {}, attributes = {}) {
    super(
      { textContent: getTextContent("signout"), ...state },
      { type: "button", ...attributes },
    );
  }

  _setStyle() {
    this.setOutlineSecondary();
    this.setSmall();
  }

  _onConnect() {
    this._attachEventListener("click", (event) => {
      event.preventDefault();
      UserSessionManager.getInstance().signOut();
    });
  }
}
