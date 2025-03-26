import { getFriends } from "../../api/users/getFriends";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { Component } from "../../core/Component";
import { setHeight } from "../../utils/elements/style/setHeight";
import { getTextContent } from "../../utils/i18n/lang";
import { UserListItem } from "../user/UserListItem";
import { ListContainer } from "../utils/ListContainer";
import { TournamentLeaveButton } from "./TournamentLeaveButton";

export class TournamentWaiting extends Component {
  #friendList;
  #leaveButton;

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setJustifyContentAround(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSizing.setWidth100(this);
    BootstrapSizing.setHeight100(this);

    setHeight(this.#friendList, "80%");
    BootstrapSizing.setWidth75(this.#leaveButton);
    this.#leaveButton.setSecondary();
  }

  _onConnect() {
    this.#friendList = new ListContainer({
      ListItem: UserListItem,
      items: [],
    });
    getFriends().then(({ users, error }) => {
      if (error) {
        this._updateState({ isError: true });
        this.#friendList = null;
        return;
      }
      this.#friendList._updateState({ items: users });
    });

    const { tournamentId } = this._getState();
    this.#leaveButton = new TournamentLeaveButton({
      textContent: getTextContent("goBack"),
      tournamentId,
    });
  }

  _render() {
    const { isError } = this._getState();
    if (isError) {
      return;
    }

    this.append(this.#friendList, this.#leaveButton);
  }
}
