import { getFriends } from "../../api/users/getFriends";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { AuthView } from "../../core/AuthView";
import { setBorderWithShadow } from "../../utils/setBorderWithShadow";
import { UserListContainer } from "../user/UserListContainer";

export class FriendsView extends AuthView {
  #friendsListContainer;

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setJustifyContentCenter(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSizing.setWidth100(this);
    BootstrapSizing.setHeight100(this);

    setBorderWithShadow(this);
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
