import { StyledButton } from "../../core/StyledButton";
import { getUserSession } from "../../session";

export class SignOutButton extends StyledButton {
  constructor(state = {}, attributes = {}) {
    super(
      { textContent: "サインアウト", ...state },
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
      event.stopPropagation();
      getUserSession().signOut();
    });
  }
}
