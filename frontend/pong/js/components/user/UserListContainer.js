import { getUsers } from "../../api/users/getUsers";
import { BootstrapGrid } from "../../bootstrap/layout/grid";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { setHeight } from "../../utils/elements/style/setHeight";
import { ErrorContainer } from "../utils/ErrorContainer";
import { ListContainer } from "../utils/ListContainer";
import { UserListItem } from "./UserListItem";
import { UserProfileContainer } from "./UserProfileContainer";

export class UserListContainer extends Component {
  #userList;
  #userProfileContainer;

  constructor(state) {
    super({ isError: false, ...state });
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

    getUsers().then(({ users, error }) => {
      if (error) {
        this._updateState({ isError: true });
        return;
      }
      this.#userList._updateState({ items: users });
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
        new ErrorContainer({ message: "ユーザー一覧情報の取得" }),
      );
      return;
    }

    this.append(this.#userList, this.#userProfileContainer);
  }
}
