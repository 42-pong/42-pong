import { BootstrapGrid } from "../../bootstrap/layout/grid";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { BootstrapText } from "../../bootstrap/utilities/text";
import { Component } from "../../core/Component";
import { createElement } from "../../utils/elements/createElement";
import { createDefaultCard } from "../../utils/elements/div/createDefaultCard";
import { createNameplate } from "../../utils/elements/div/createNameplate";
import { AddFriendButton } from "../friend/AddFriendButton";
import { BlockUserButton } from "./BlockUserButton";

export class UserProfile extends Component {
  constructor(state) {
    super({ userId: "", user: null, ...state });
  }

  _setStyle() {
    BootstrapSizing.setWidth50(this);
    BootstrapText.setTextCenter(this);
  }

  _render() {
    const { user } = this._getState();

    if (!user) {
      const placeholderText = createElement("span", {
        textContent: "ユーザーを選択してください",
      });
      this.append(placeholderText);
      return;
    }

    const nameplate = createNameplate(user);
    const profileButtonPanel = createProfileMenu();
    this.append(
      createDefaultCard({
        title: nameplate,
        others: [profileButtonPanel],
      }),
    );
  }
}

const createProfileMenu = () => {
  const addFriendButton = new AddFriendButton();
  addFriendButton.setPrimary();
  styleProfileButton(addFriendButton);

  const blockUserButton = new BlockUserButton();
  blockUserButton.setDanger();
  styleProfileButton(blockUserButton);

  const buttonPanel = createElement("div");
  BootstrapGrid.setRow(buttonPanel);
  BootstrapFlex.setJustifyContentCenter(buttonPanel);
  buttonPanel.append(addFriendButton, blockUserButton);

  return buttonPanel;
};

const styleProfileButton = (button) => {
  BootstrapGrid.setCol(button, 10);
  BootstrapGrid.setCol(button, 5, "xl");
  BootstrapSpacing.setMargin(button);
};
