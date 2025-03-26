import { Paths } from "../../constants/Paths";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { UserSessionManager } from "../../session/UserSessionManager";
import { createDefaultNavbar } from "../../utils/elements/nav/createDefaultNavbar";
import { createGuestNavbar } from "../../utils/elements/nav/createGuestNavbar";

export class MainNavbar extends Component {
  #listenIsSignedIn;

  static links = Object.freeze([
    { name: "home", path: Paths.HOME },
    { name: "usersList", path: Paths.USERS },
    { name: "friendsList", path: Paths.FRIENDS },
    { name: "dashboard", path: Paths.DASHBOARD },
    { name: "mypage", path: Paths.MYPAGE },
  ]);

  constructor(state = {}) {
    super(state);

    this.#listenIsSignedIn = null;
  }

  _onConnect() {
    const isSignedIn =
      UserSessionManager.getInstance().myInfo.observe(
        ({ isSignedIn }) => isSignedIn,
      );
    Object.assign(this._state, { isSignedIn });

    this._attachEventListener(
      "click",
      PongEvents.UPDATE_ROUTER.trigger,
    );

    this.#listenIsSignedIn = ({ isSignedIn }) => {
      this._updateState({ isSignedIn });
    };
    UserSessionManager.getInstance().myInfo.attach(
      this.#listenIsSignedIn,
    );
  }

  _onDisconnect() {
    UserSessionManager.getInstance().myInfo.detach(
      this.#listenIsSignedIn,
    );
    this.#listenIsSignedIn = null;
  }

  _render() {
    const { isSignedIn } = this._getState();

    const navbar = isSignedIn
      ? createDefaultNavbar(MainNavbar.links)
      : createGuestNavbar();
    this.append(navbar);
  }
}
