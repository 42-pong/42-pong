import { patchMyInfo } from "../../api/users/patchMyInfo";
import { BootstrapButtons } from "../../bootstrap/components/buttons";
import { BootstrapBorders } from "../../bootstrap/utilities/borders";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Component } from "../../core/Component";
import { UserSessionManager } from "../../session/UserSessionManager";
import { createButton } from "../../utils/elements/button/createButton";
import { createElement } from "../../utils/elements/createElement";
import { createThreeColumnLayout } from "../../utils/elements/div/createThreeColumnLayout";
import { createTextElement } from "../../utils/elements/span/createTextElement";
import { createDefaultUnorderedList } from "../../utils/elements/ul/createDefaultUnorderedList";

export class MyInfoContainer extends Component {
  #displayInput;

  _onConnect() {
    this.#displayInput = createElement("input", {}, { type: "text" });

    this._attachEventListener("click", async (event) => {
      event.preventDefault();
      const {
        target: { name },
      } = event;
      if (name !== "displayName") return;
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
    });
  }

  _render() {
    const { displayName, email, avatar, username } =
      UserSessionManager.getInstance().myInfo.observe(
        (myInfo) => myInfo,
      );
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

    const inputList = createDefaultUnorderedList([
      displayNameInput,
      usernameInput,
      emailInput,
    ]);

    BootstrapDisplay.setGrid(inputList);
    BootstrapSizing.setWidth50(inputList);
    BootstrapSpacing.setGap(inputList);
    BootstrapSizing.setWidth100(inputList);
    this.append(inputList);
  }
}

const createInputField = (labelName, placeholder, setButtonStyle) => {
  const label = createTextElement(labelName, 6);
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

  return createThreeColumnLayout(label, input, button, 4, 4, 1);
};

const createDisplayInputField = (displayInput) => {
  const label = createTextElement("表示名", 6);
  const button = createButton(
    { textContent: "保存" },
    { type: "submit", name: "displayName" },
  );
  BootstrapButtons.setPrimary(button);
  BootstrapButtons.setSmall(button);

  return createThreeColumnLayout(
    label,
    displayInput,
    button,
    4,
    4,
    1,
  );
};
