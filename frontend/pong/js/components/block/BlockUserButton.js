import { postBlocks } from "../../api/users/postBlocks";
import { StyledButton } from "../../core/StyledButton";

export class BlockUserButton extends StyledButton {
  constructor(state = {}, attributes = {}) {
    super(
      { textContent: "ブロック", user: null, reload: null, ...state },
      { type: "button", ...attributes },
    );
  }

  _setStyle() {
    this.setOutlineDanger();
    const {
      user: { isBlocked },
    } = this._getState();
    if (isBlocked) {
      this.setDisabled();
      this.setTextContent("ブロック済み");
    } else {
      this.unsetDisabled();
      this.setTextContent("ブロック");
    }
  }

  _onConnect() {
    const { user, reload } = this._getState();
    if (!(user && reload)) {
      this.setTextContent("...");
      return;
    }

    this._attachEventListener("click", (event) => {
      event.preventDefault();
      const {
        user: { id, isBlocked },
        reload,
      } = this._getState();
      if (isBlocked) return;
      postBlocks(id).then(({ user, error }) => {
        if (error) return;
        reload();
      });
    });
  }
}
