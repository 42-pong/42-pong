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
  }

  _onConnect() {
    const { user, reload } = this._getState();
    if (!(user && reload)) {
      this.setTextContent("...");
      return;
    }

    const { id } = user;
    this._attachEventListener("click", (event) => {
      event.preventDefault();
      deleteFriends(id).then(({ error }) => {
        if (error) return;
        reload();
      });
    });
  }
}
