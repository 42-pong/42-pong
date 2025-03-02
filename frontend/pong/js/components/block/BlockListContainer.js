import { getBlocks } from "../../api/users/getBlocks";
import { BootstrapBadge } from "../../bootstrap/components/badge";
import { BootstrapBorders } from "../../bootstrap/utilities/borders";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Component } from "../../core/Component";
import { createDefaultFlexBox } from "../../utils/elements/div/createFlexBox";
import { createHorizontalSplitLayout } from "../../utils/elements/div/createHorizontalSplitLayout";
import { createTextElement } from "../../utils/elements/span/createTextElement";
import { setHeight } from "../../utils/elements/style/setHeight";
import { ListContainer } from "../utils/ListContainer";
import { BlockListItem } from "./BlockListItem";

export class BlockListContainer extends Component {
  #blockList;

  constructor(state = {}) {
    super({ items: [], ...state });
  }

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapFlex.setJustifyContentCenter(this);
  }

  _onConnect() {
    getBlocks().then(({ users, error }) => {
      if (error) {
        this._updateState({ isError: true });
        return;
      }
      this._updateState({ items: users });
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

    const { items } = this._getState();
    const blockPanel =
      items.length > 0 ? createBlockList(items) : noBlockedUser();

    const layout = createHorizontalSplitLayout(title, blockPanel);
    BootstrapSpacing.setPadding(layout, 3);
    BootstrapSizing.setWidth100(layout);
    BootstrapSizing.setHeight100(layout);
    BootstrapSpacing.setMargin(title);
    this.append(layout);
  }
}

const noBlockedUser = () => {
  const content = createTextElement(
    "ユーザーが見つかりませんでした",
    5,
    BootstrapBadge.setSecondary,
  );
  const wrapper = createDefaultFlexBox(content);
  setHeight(wrapper, "50vh");
  BootstrapSpacing.setPadding(wrapper, 3);
  return wrapper;
};

const createBlockList = (items) => {
  const blockList = new ListContainer({
    ListItem: BlockListItem,
    items,
  });
  setHeight(blockList, "50vh");
  BootstrapSizing.setWidth100(blockList);
  BootstrapSpacing.setMargin(blockList);
  return blockList;
};
