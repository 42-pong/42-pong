import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { AuthView } from "../../core/AuthView";
import { createVerticalSplitLayout } from "../../utils/elements/div/createVerticalSplitLayout";
import { BlockListContainer } from "../block/BlockListContainer";
import { MyInfoContainer } from "../user/MyInfoContainer";

export class MyPageView extends AuthView {
  #myInfo;
  #blockListContainer;

  _onConnect() {
    this.#myInfo = new MyInfoContainer();
    this.#blockListContainer = new BlockListContainer();
  }

  _render() {
    const { isError } = this._getState();
    if (isError) {
      this.append(new ErrorContainer({ message: "一覧情報の取得" }));
      return;
    }

    const splitLayout = createVerticalSplitLayout(
      this.#myInfo,
      this.#blockListContainer,
      6,
      4,
    );
    BootstrapSizing.setHeight100(splitLayout);
    this.append(splitLayout);
  }
}
