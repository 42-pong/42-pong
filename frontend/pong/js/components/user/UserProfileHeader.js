import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Component } from "../../core/Component";
import { getUserSession } from "../../session";
import { createNameplate } from "../../utils/elements/div/createNameplate";
import { SignInButton } from "../auth/SignInButton";
import { SignOutButton } from "../auth/SignOutButton";

export class UserProfileHeader extends Component {
  #userDataObserver;

  constructor(state = {}) {
    super(state);
    this.#userDataObserver = (myInfoData) => {
      const { isSignedIn, id, username, displayName, avatar } =
        myInfoData;

      const user = isSignedIn
        ? { id, username, displayName, avatar }
        : null;

      this._updateState({ user });
    };
  }

  _setStyle() {
    BootstrapDisplay.setFlex(this);
  }

  _onConnect() {
    getUserSession().myInfoManager.attach(this.#userDataObserver);
  }

  _onDisconnect() {
    getUserSession().myInfoManager.detach(this.#userDataObserver);
  }

  _render() {
    const { user } = this._getState();
    if (!user) {
      this.append(new SignInButton());
      return;
    }

    const nameplate = createNameplate(user, "4vh");
    const signOutButton = new SignOutButton();
    BootstrapSpacing.setMarginLeft(signOutButton, 3);

    this.append(nameplate, signOutButton);
  }
}
