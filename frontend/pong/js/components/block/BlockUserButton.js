import { postBlocks } from "../../api/users/postBlocks";
import { StyledButton } from "../../core/StyledButton";
import { getTextContent } from "../../utils/i18n/lang";

export class BlockUserButton extends StyledButton {
  constructor(state = {}, attributes = {}) {
    super(
      {
        textContent: getTextContent("blockUser"),
        user: null,
        reload: null,
        ...state,
      },
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
      this.setTextContent(getTextContent("alreadyBlocked"));
    } else {
      this.unsetDisabled();
      this.setTextContent(getTextContent("blockUser"));
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

      this.setTextContent("...");
      postBlocks(id).then(({ error }) => {
        if (error) return;
        reload();
      });
    });
  }
}
