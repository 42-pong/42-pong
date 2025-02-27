import { postFriends } from "../../api/users/postFriends";
import { StyledButton } from "../../core/StyledButton";

export class AddFriendButton extends StyledButton {
  constructor(state = {}, attributes = {}) {
    super(
      {
        textContent: "フレンド追加",
        user: null,
        reload: null,
        ...state,
      },
      { type: "button", ...attributes },
    );
  }

  _setStyle() {
    this.setPrimary();
    const {
      user: { isBlocked },
    } = this._getState();
    if (isBlocked) this.setDisabled();
    else this.unsetDisabled();
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
      postFriends(id).then(({ user, error }) => {
        if (error) return;
        reload();
      });
    });
  }
}
