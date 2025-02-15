import { getFriends } from "../../api/users/getFriends";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { View } from "../../core/View";
import { UserListContainer } from "../user/UserListContainer";

export class FriendsView extends View {
  #friendsListContainer;

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setJustifyContentCenter(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSizing.setWidth100(this);
    BootstrapSizing.setHeight100(this);
  }

  _onConnect() {
    this.#friendsListContainer = new UserListContainer({
      fetchUsers: getFriends,
    });
  }

  _render() {
    this.append(this.#friendsListContainer);
  }
}
