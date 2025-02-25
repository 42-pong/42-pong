import { Paths } from "../../constants/Paths";
import { PongEvents } from "../../constants/PongEvents";
import { StyledButton } from "../../core/StyledButton";

export class SignUpButton extends StyledButton {
  constructor(state = {}, attributes = {}) {
    super(
      { textContent: "サインアップ", ...state },
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

      this.dispatchEvent(
        PongEvents.UPDATE_ROUTER.create(Paths.SIGNUP),
      );
    });
  }
}
