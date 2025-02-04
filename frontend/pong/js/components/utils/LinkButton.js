import { Paths } from "../../constants/Paths";
import { PongEvents } from "../../constants/PongEvents";
import { StyledButton } from "../../core/StyledButton";

export class LinkButton extends StyledButton {
  constructor(state = {}, attributes = {}) {
    super(
      { textContent: "link", pathname: Paths.HOME, ...state },
      { type: "button", ...attributes },
    );
  }

  _onConnect() {
    this._attachEventListener(
      "click",
      PongEvents.UPDATE_ROUTER.trigger,
    );
  }
}
