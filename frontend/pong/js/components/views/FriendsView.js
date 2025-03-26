import { getFriends } from "../../api/users/getFriends";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { AuthView } from "../../core/AuthView";
import { UserSessionManager } from "../../session/UserSessionManager";
import { UserListContainer } from "../user/UserListContainer";

export class FriendsView extends AuthView {
  #friendsListContainer;
  #reloadList;

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
    this.#reloadList = () => {
      this.#friendsListContainer.reloadList();
    };
    UserSessionManager.getInstance().status.attach(this.#reloadList);
  }

  _onDisconnect() {
    UserSessionManager.getInstance().status.detach(this.#reloadList);
  }

  _render() {
    this.append(this.#friendsListContainer);
  }
}
