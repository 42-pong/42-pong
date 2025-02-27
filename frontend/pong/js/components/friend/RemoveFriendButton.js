import { deleteFriends } from "../../api/users/deleteFriends";
import { StyledButton } from "../../core/StyledButton";

export class RemoveFriendButton extends StyledButton {
  constructor(state = {}, attributes = {}) {
    super(
      {
        textContent: "フレンド解除",
        user: null,
        reload: null,
        ...state,
      },
      { type: "button", ...attributes },
    );
  }

  _setStyle() {
    this.setOutlinePrimary();
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
      deleteFriends(id).then(({ error }) => {
        if (error) return;
        reload();
      });
    });
  }
}
