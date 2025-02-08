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

  _onConnect() {}

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

    const addFriendButton = new AddFriendButton();
    addFriendButton.setPrimary();
    BootstrapGrid.setCol(addFriendButton, 10);
    BootstrapGrid.setCol(addFriendButton, 5, "xl");
    BootstrapSpacing.setMargin(addFriendButton);

    const blockUserButton = new BlockUserButton();
    blockUserButton.setDanger();
    BootstrapGrid.setCol(blockUserButton, 10);
    BootstrapGrid.setCol(blockUserButton, "5", "xl");
    BootstrapSpacing.setMargin(blockUserButton);

    const buttons = createElement("div");
    BootstrapGrid.setRow(buttons);
    BootstrapFlex.setJustifyContentCenter(buttons);
    buttons.append(addFriendButton, blockUserButton);

    this.appendChild(
      createDefaultCard({
        title: nameplate,
        others: [buttons],
      }),
    );
  }
}
