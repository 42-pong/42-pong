import { StyledButton } from "../../core/StyledButton";

export class AddFriendButton extends StyledButton {
  constructor(state = {}, attributes = {}) {
    super(
      { textContent: "フレンド追加", ...state },
      { type: "button", ...attributes },
    );
  }
}
