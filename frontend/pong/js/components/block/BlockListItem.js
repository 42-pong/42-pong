import { getUser } from "../../api/users/getUser";
import { Component } from "../../core/Component";
import { createAroundFlexBox } from "../../utils/elements/div/createFlexBox";
import { createNameplate } from "../../utils/elements/div/createNameplate";
import { createVerticalSplitLayout } from "../../utils/elements/div/createVerticalSplitLayout";
import { UnblockUserButton } from "./UnblockUserButton";

export class BlockListItem extends Component {
  #reload() {
    const { item: user } = this._getState();
    getUser(user.id).then(({ user, error }) => {
      if (error) return;
      this._updateState({ item: user });
    });
  }

  _render() {
    const { item: user } = this._getState();
    const nameplate = createNameplate(user, "max(30px,4vh)");
    this.append(
      createVerticalSplitLayout(
        nameplate,
        new UnblockUserButton({
          user,
          reload: this.#reload.bind(this),
        }),
        8,
        2,
      ),
    );
  }
}
