import { patchMyInfo } from "../../api/users/patchMyInfo";
import { BootstrapButtons } from "../../bootstrap/components/buttons";
import { BootstrapBorders } from "../../bootstrap/utilities/borders";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { UserSessionManager } from "../../session/UserSessionManager";
import { createButton } from "../../utils/elements/button/createButton";
import { createElement } from "../../utils/elements/createElement";
import { createAroundFlexBox } from "../../utils/elements/div/createFlexBox";
import { createTextElement } from "../../utils/elements/span/createTextElement";
import { EventDispatchingButton } from "../utils/EventDispatchingButton";
import { MyInfoAvatar } from "./MyInfoAvatar";

export class MyInfoContainer extends Component {
  #displayInput;

  _onConnect() {
    this.#displayInput = createElement("input", {}, { type: "text" });

    this._attachEventListener(
      PongEvents.PATCH_DISPLAY_NAME.type,
      async (event) => {
        event.preventDefault();
        const { error } = await patchMyInfo({
          displayName: this.#displayInput.value,
        });
        if (error) {
          BootstrapBorders.setDanger(this.#displayInput);
          return;
        }
        BootstrapBorders.unsetDanger(this.#displayInput);
        await UserSessionManager.getInstance().verifyAuth();
        this._updateState();
      },
    );
  }

  _render() {
    const myInfo = UserSessionManager.getInstance().myInfo.observe(
      (myInfo) => myInfo,
    );

    const avatarImage = new MyInfoAvatar({
      user: myInfo,
      height: "max(100px,15vh)",
    });
    const { displayName, email, username } = myInfo;
    this.#displayInput.value = displayName;
    const displayNameInput = createDisplayInputField(
      this.#displayInput,
    );

    const usernameInput = createInputField(
      "ユーザー名",
      username,
      BootstrapButtons.setOutlinePrimary,
    );

    const emailInput = createInputField(
      "メール",
      email,
      BootstrapButtons.setOutlinePrimary,
    );

    const inputList = createAroundFlexBox(
      avatarImage,
      displayNameInput,
      usernameInput,
      emailInput,
    );
    BootstrapFlex.setFlexColumn(inputList);
    BootstrapDisplay.setGrid(inputList);
    BootstrapSpacing.setGap(inputList);
    BootstrapSizing.setWidth100(inputList);
    this.append(inputList);
  }
}

const createInputField = (labelName, placeholder, setButtonStyle) => {
  const label = createTextElement(labelName, 6);
  BootstrapSizing.setWidth25(label);
  const input = createElement(
    "input",
    { type: "text", value: placeholder },
    { disabled: "" },
  );
  const button = createButton(
    { textContent: "保存" },
    { disabled: "" },
  );
  setButtonStyle(button);
  BootstrapButtons.setSmall(button);

  const layout = createAroundFlexBox(label, input, button);
  BootstrapSizing.setWidth75(layout);
  return layout;
};

const createDisplayInputField = (displayInput) => {
  const label = createTextElement("表示名", 6);
  BootstrapSizing.setWidth25(label);
  const patchDisplayName = new EventDispatchingButton(
    { textContent: "保存" },
    {},
    PongEvents.PATCH_DISPLAY_NAME,
  );
  patchDisplayName.setPrimary();
  patchDisplayName.setSmall();

  const layout = createAroundFlexBox(
    label,
    displayInput,
    patchDisplayName,
  );
  BootstrapSizing.setWidth75(layout);
  return layout;
};
