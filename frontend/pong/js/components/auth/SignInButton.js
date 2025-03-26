import { Paths } from "../../constants/Paths";
import { PongEvents } from "../../constants/PongEvents";
import { StyledButton } from "../../core/StyledButton";
import { getTextContent } from "../../utils/i18n/lang";

export class SignInButton extends StyledButton {
  constructor(state = {}, attributes = {}) {
    super(
      { textContent: getTextContent("signin"), ...state },
      { type: "button", ...attributes },
    );
  }

  _onConnect() {
    this._attachEventListener("click", (event) => {
      event.preventDefault();

      this.dispatchEvent(
        PongEvents.UPDATE_ROUTER.create(Paths.LOGIN),
      );
    });
  }
}
