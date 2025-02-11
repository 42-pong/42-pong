import { getUser } from "../../api/users/getUser";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { Component } from "../../core/Component";
import { ErrorContainer } from "../utils/ErrorContainer";
import { UserProfile } from "./UserProfile";

export class UserProfileContainer extends Component {
  #userProfile;

  constructor(state) {
    super({ isError: false, ...state });
  }
  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapFlex.setJustifyContentCenter(this);
  }

  _onConnect() {
    this.#userProfile = new UserProfile({ userId: "" });
  }

  _render() {
    const { isError } = this._getState();
    if (isError) {
      this.append(
        new ErrorContainer({ message: "ユーザー情報の取得" }),
      );
      return;
    }

    this.append(this.#userProfile);
  }

  setUserId(userId) {
    if (!this.#userProfile) return;

    getUser(userId).then(({ user, error }) => {
      if (error) {
        this._updateState({ isError: true });
        return;
      }
      this.#userProfile._updateState({ user });
    });
  }
}
