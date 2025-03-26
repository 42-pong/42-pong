import { getUser } from "../../api/users/getUser";
import { BootstrapBadge } from "../../bootstrap/components/badge";
import { BootstrapGrid } from "../../bootstrap/layout/grid";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { BootstrapText } from "../../bootstrap/utilities/text";
import { Component } from "../../core/Component";
import { UserSessionManager } from "../../session/UserSessionManager";
import { createElement } from "../../utils/elements/createElement";
import { createDefaultCard } from "../../utils/elements/div/createDefaultCard";
import { createNameplate } from "../../utils/elements/div/createNameplate";
import { createTextElement } from "../../utils/elements/span/createTextElement";
import { getTextContent } from "../../utils/i18n/lang";
import { BlockUserButton } from "../block/BlockUserButton";
import { AddFriendButton } from "../friend/AddFriendButton";
import { RemoveFriendButton } from "../friend/RemoveFriendButton";

export class UserProfile extends Component {
  #reload;

  constructor(state) {
    super({ user: null, ...state });
    this.#reload = () => {
      const { user } = this._getState();
      if (!user) return;

      const { id } = user;
      getUser(id).then(({ user, error }) => {
        if (error) return;
        this._updateState({ user });
      });
    };
  }

  _setStyle() {
    BootstrapSizing.setWidth50(this);
    BootstrapText.setTextCenter(this);
  }

  _render() {
    const { user } = this._getState();
    if (!user) {
      const placeholderText = createTextElement(
        "ユーザーを選択してください",
        5,
        BootstrapBadge.setPrimary,
      );
      this.append(placeholderText);
      return;
    }

    const nameplate = createNameplate(user, "max(60px,8vh)");
    const isMe =
      UserSessionManager.getInstance().myInfo.observe(
        ({ id }) => id,
      ) === user.id;

    const matchResult = createTextElement(
      `${getTextContent("win")} ${user.matchWins} | ${getTextContent("loss")} ${user.matchLosses}`,
      5,
      BootstrapBadge.setWarning,
    );
    BootstrapSpacing.setMargin(matchResult, 2);
    const profileButtonPanel = createProfileMenu(user, this.#reload);
    this.append(
      createDefaultCard({
        title: nameplate,
        text: matchResult,
        others: isMe ? [] : [profileButtonPanel],
      }),
    );
  }
}

const createProfileMenu = (user, reload) => {
  const { isFriend } = user;

  const FriendButton = isFriend
    ? RemoveFriendButton
    : AddFriendButton;
  const friendButton = new FriendButton({ user, reload });
  styleProfileButton(friendButton);

  const blockUserButton = new BlockUserButton({ user, reload });
  styleProfileButton(blockUserButton);

  const buttonPanel = createElement("div");
  BootstrapGrid.setRow(buttonPanel);
  BootstrapFlex.setJustifyContentCenter(buttonPanel);
  buttonPanel.append(friendButton, blockUserButton);

  return buttonPanel;
};

const styleProfileButton = (button) => {
  BootstrapGrid.setCol(button, 10);
  BootstrapGrid.setCol(button, 5, "xl");
  BootstrapSpacing.setMargin(button);
};
