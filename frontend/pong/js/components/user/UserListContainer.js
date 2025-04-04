import { getUsers } from "../../api/users/getUsers";
import { BootstrapBadge } from "../../bootstrap/components/badge";
import { BootstrapGrid } from "../../bootstrap/layout/grid";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { createTextElement } from "../../utils/elements/span/createTextElement";
import { setHeight } from "../../utils/elements/style/setHeight";
import { getTextContent } from "../../utils/i18n/lang";
import { ErrorContainer } from "../utils/ErrorContainer";
import { ListContainer } from "../utils/ListContainer";
import { UserListItem } from "./UserListItem";
import { UserProfileContainer } from "./UserProfileContainer";

export class UserListContainer extends Component {
  #userList;
  #userProfileContainer;

  constructor(state) {
    super({
      isError: false,
      fetchUsers: getUsers,
      users: [],
      ...state,
    });
  }

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapFlex.setJustifyContentCenter(this);
    BootstrapSizing.setWidth100(this);
    BootstrapSizing.setHeight100(this);

    setHeight(this.#userList, "75vh");
    BootstrapGrid.setCol(this.#userList, "3");
    BootstrapGrid.setCol(this.#userProfileContainer, "7");
  }

  _onConnect() {
    this.#userList = new ListContainer({
      ListItem: UserListItem,
      items: [],
    });
    this.#userProfileContainer = new UserProfileContainer();

    const { fetchUsers } = this._getState();
    fetchUsers().then(({ users, error }) => {
      if (error) {
        this._updateState({ isError: true });
        return;
      }
      this._updateState({ users });
    });

    this._attachEventListener(
      PongEvents.UPDATE_USER_ID.type,
      (event) => {
        const {
          detail: { userId },
        } = event;
        this.#userProfileContainer.setUserId(userId);
      },
    );
  }

  _render() {
    const { isError } = this._getState();
    if (isError) {
      this.append(
        new ErrorContainer({
          message: getTextContent("getListInformation"),
        }),
      );
      return;
    }

    const { users } = this._getState();
    if (users.length === 0) {
      const placeholderText = createTextElement(
        getTextContent("noUserAnnouncement"),
        5,
        BootstrapBadge.setSecondary,
      );
      this.append(placeholderText);
      return;
    }

    Object.assign(this.#userList._getState(), { items: users });
    this.append(this.#userList, this.#userProfileContainer);
  }

  reloadList() {
    if (this.#userList) this.#userList._updateState();
  }
}
