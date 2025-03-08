import { startOauth } from "../../api/utils/startOauth";
import { StyledButton } from "../../core/StyledButton";

export class OauthButton extends StyledButton {
  constructor(state = {}, attributes = {}) {
    super(
      { textContent: "42 OAuth 2.0", ...state },
      { type: "button", ...attributes },
    );
  }

  _setStyle() {
    this.setSuccess();
  }

  _onConnect() {
    this._attachEventListener("click", async (event) => {
      event.preventDefault();
      await startOauth();
    });
  }
}
