import { StyledButton } from "../../core/StyledButton";

export class BlockUserButton extends StyledButton {
  constructor(state = {}, attributes = {}) {
    super(
      { textContent: "ブロック", ...state },
      { type: "button", ...attributes },
    );
  }
}
