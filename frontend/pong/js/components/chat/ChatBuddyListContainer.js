import { getFriends } from "../../api/users/getFriends";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Component } from "../../core/Component";
import { createElement } from "../../utils/elements/createElement";
import { UserListItem } from "../user/UserListItem";
import { ListContainer } from "../utils/ListContainer";

export class ChatBuddyListContainer extends Component {
  constructor(state = {}) {
    super({ isError: false, buddyList: [], ...state });
  }

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setJustifyContentAround(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSizing.setWidth100(this);
    BootstrapSizing.setHeight100(this);
    BootstrapSpacing.setPadding(this);
  }

  _onConnect() {
    // TODO: users は フレンド + チャット進行中のユーザー
    getFriends().then(({ users, error }) => {
      if (error) {
        this._updateState({ isError: true });
        return;
      }
      this._updateState({ buddyList: users });
    });
  }

  _render() {
    const { isError, buddyList } = this._getState();
    if (isError) {
      const errorMessage = createElement("span", {
        textContent: "❗ Error: チャットエラー",
      });
      this.append(errorMessage);
      return;
    }

    const buddyListElement = new ListContainer({
      ListItem: UserListItem,
      items: buddyList,
    });
    BootstrapSizing.setHeight100(buddyListElement);
    BootstrapSizing.setWidth100(buddyListElement);

    this.append(buddyListElement);
  }
}
