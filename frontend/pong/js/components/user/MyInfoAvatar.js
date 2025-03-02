import { patchAvatar } from "../../api/users/patchAvatar";
import { BootstrapBorders } from "../../bootstrap/utilities/borders";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { UserSessionManager } from "../../session/UserSessionManager";
import { createElement } from "../../utils/elements/createElement";
import { createHorizontalSplitLayout } from "../../utils/elements/div/createHorizontalSplitLayout";
import { createAvatarImage } from "../../utils/user/createAvatarImage";
import { formatUserInfo } from "../../utils/user/formatUserInfo";
import { EventDispatchingButton } from "../utils/EventDispatchingButton";

export class MyInfoAvatar extends Component {
  #reload;
  #input;
  #button;
  #updateAvatarPanel;

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setJustifyContentCenter(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSpacing.setMargin(this, 5);
    BootstrapBorders.setBorder(this.#updateAvatarPanel);
    BootstrapBorders.setRounded(this.#updateAvatarPanel);
    BootstrapSpacing.setMargin(this.#updateAvatarPanel);
    BootstrapSpacing.setPadding(this.#updateAvatarPanel);
    this.#button.setPrimary();
    this.#button.setSmall();
  }

  _onConnect() {
    this._attachEventListener(
      PongEvents.PATCH_AVATAR.type,
      async () => {
        const avatar = this.#input.files[0];
        const { error } = await patchAvatar(avatar);
        if (error) {
          BootstrapBorders.setDanger(this.#updateAvatarPanel);
          return;
        }
        BootstrapBorders.unsetDanger(this.#updateAvatarPanel);
        await UserSessionManager.getInstance().verifyAuth();
        this._updateState();
      },
    );

    this.#input = createElement(
      "input",
      {},
      { type: "file", name: "avatar" },
    );
    this.#button = new EventDispatchingButton(
      {
        textContent: "アップロード",
      },
      {},
      PongEvents.PATCH_AVATAR,
    );
    this.#updateAvatarPanel = createHorizontalSplitLayout(
      this.#input,
      this.#button,
    );

    this.#reload = () => this._updateState();
    UserSessionManager.getInstance().myInfo.attach(this.#reload);
  }

  _onDisconnect() {
    UserSessionManager.getInstance().myInfo.detach(this.#reload);
  }

  _render() {
    const { height } = this._getState();
    const myInfo = UserSessionManager.getInstance().myInfo.observe(
      (myInfo) => myInfo,
    );
    // ✏️

    const { avatarPathname, avatarAlt } = formatUserInfo(myInfo);

    const avatar = createAvatarImage({
      pathname: avatarPathname,
      alt: avatarAlt,
      height,
    });
    // const submit = createButton({textContent: "Upload"}, {type: "submit"})
    // const form = createElement("form", {}, {id:"formId"});
    // form.append(this.#input, submit);
    this.append(avatar, this.#updateAvatarPanel);
  }
}
