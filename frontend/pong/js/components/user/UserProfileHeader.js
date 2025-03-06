import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Component } from "../../core/Component";
import { UserSessionManager } from "../../session/UserSessionManager";
import { createNameplate } from "../../utils/elements/div/createNameplate";
import { SignInButton } from "../auth/SignInButton";
import { SignOutButton } from "../auth/SignOutButton";
import { SignUpButton } from "../auth/SignUpButton";
import { LangSelector } from "../utils/LangSelector";

export class UserProfileHeader extends Component {
  #userDataObserver;

  constructor(state = {}) {
    super(state);
    this.#userDataObserver = (myInfoData) => {
      this._updateState({ user: createUser(myInfoData) });
    };
  }

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapFlex.setJustifyContentCenter(this);
  }

  _onConnect() {
    UserSessionManager.getInstance().myInfo.observe((myInfoData) => {
      Object.assign(this._state, { user: createUser(myInfoData) });
    });
    UserSessionManager.getInstance().myInfo.attach(
      this.#userDataObserver,
    );
  }

  _onDisconnect() {
    UserSessionManager.getInstance().myInfo.detach(
      this.#userDataObserver,
    );
  }

  _render() {
    const { user } = this._getState();

    const langSelector = new LangSelector();
    BootstrapSpacing.setMarginLeft(langSelector, 3);

    if (!user) {
      const signIn = new SignInButton();
      signIn.setOutlinePrimary();
      signIn.setSmall();
      const signUp = new SignUpButton();
      signUp.setPrimary();
      signUp.setSmall();
      BootstrapSpacing.setMarginLeft(signUp, 3);
      this.append(signIn, signUp, langSelector);
      return;
    }

    const nameplate = createNameplate(user, "max(30px,4vh)");
    const signOutButton = new SignOutButton();
    BootstrapSpacing.setMarginLeft(signOutButton, 3);

    this.append(nameplate, signOutButton, langSelector);
  }
}

const createUser = (myInfoData) => {
  const { isSignedIn, id, username, displayName, avatar } =
    myInfoData;
  const user = isSignedIn
    ? { id, username, displayName, avatar }
    : null;
  return user;
};
