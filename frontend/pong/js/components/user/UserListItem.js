import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { createNameplate } from "../../utils/elements/div/createNameplate";

// TODO: avatar 表示
export class UserListItem extends Component {
  _onConnect() {
    this.setAttribute("role", "button");
    this._attachEventListener("click", (event) => {
      event.preventDefault();
      const {
        item: { id: userId },
      } = this._getState();
      if (!userId) return;

      this.dispatchEvent(PongEvents.UPDATE_USER_ID.create(userId));
    });
  }

  _render() {
    const { item: user } = this._getState();
    this.append(createNameplate(user));
  }
}
