import { getBlocks } from "../../api/users/getBlocks";
import { BootstrapBadge } from "../../bootstrap/components/badge";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Component } from "../../core/Component";
import { createHorizontalSplitLayout } from "../../utils/elements/div/createHorizontalSplitLayout";
import { createTextElement } from "../../utils/elements/span/createTextElement";
import { setHeight } from "../../utils/elements/style/setHeight";
import { ListContainer } from "../utils/ListContainer";
import { BlockListItem } from "./BlockListItem";

export class BlockListContainer extends Component {
  #blockList;

  constructor(state = {}) {
    super(state);
    this.#blockList = null;
  }

  _setStyle() {
    setHeight(this.#blockList, "50vh");
    BootstrapSizing.setWidth100(this.#blockList);
    BootstrapSpacing.setMargin(this.#blockList);
  }

  _onConnect() {
    this.#blockList = new ListContainer({
      ListItem: BlockListItem,
      items: [],
    });

    getBlocks().then(({ users, error }) => {
      if (error) {
        this._updateState({ isError: true });
        return;
      }
      if (this.#blockList)
        this.#blockList._updateState({ items: users });
    });
  }

  _render() {
    const { isError } = this._getState();
    if (isError) {
      this.append(
        createTextElement(
          "ブロック情報の取得",
          5,
          BootstrapBadge.setWarning,
        ),
      );
      return;
    }

    const title = createTextElement(
      "ブロック一覧",
      5,
      BootstrapBadge.setDanger,
    );
    const layout = createHorizontalSplitLayout(
      title,
      this.#blockList,
    );
    BootstrapSizing.setHeight100(layout);
    BootstrapSpacing.setMargin(title);
    this.append(layout);
  }
}
