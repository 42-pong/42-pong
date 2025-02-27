import { getMyInfo } from "../../api/users/getMyInfo";
import { getUser } from "../../api/users/getUser";
import { BootstrapBadge } from "../../bootstrap/components/badge";
import { BootstrapButtons } from "../../bootstrap/components/buttons";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Component } from "../../core/Component";
import { UserSessionManager } from "../../session/UserSessionManager";
import { createButton } from "../../utils/elements/button/createButton";
import { createElement } from "../../utils/elements/createElement";
import { createStartFlexBox } from "../../utils/elements/div/createFlexBox";
import { createThreeColumnLayout } from "../../utils/elements/div/createThreeColumnLayout";
import { createTextElement } from "../../utils/elements/span/createTextElement";
import { createDefaultUnorderedList } from "../../utils/elements/ul/createDefaultUnorderedList";

export class MyInfoContainer extends Component {
  #input;
  #button;
  #form;

  _render() {
    UserSessionManager.getInstance()
      .verifyAuth()
      .then((isVerified) => {
        if (!isVerified) {
          this.append("...");
          return;
        }
      });

    const reload = () => this._updateState();

    const { displayName, email, avatar, username } =
      UserSessionManager.getInstance().myInfo.observe(
        (myInfo) => myInfo,
      );
    const displayNameInput = createInputField(
      "表示名",
      displayName,
      reload,
      true,
      BootstrapButtons.setPrimary,
    );

    const usernameInput = createInputField(
      "username",
      username,
      reload,
      false,
      BootstrapButtons.setOutlinePrimary,
    );

    const emailInput = createInputField(
      "email",
      email,
      reload,
      false,
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

const createInputField = (
  labelName,
  placeholder,
  onSubmit,
  isEditable,
  setButtonStyle,
) => {
  const label = createTextElement(labelName, 6);
  const input = createElement(
    "input",
    { type: "text", value: placeholder },
    { disabled: "" },
  );
  const button = createButton(
    { textContent: "保存" },
    { type: "submit", disabled: "" },
  );
  setButtonStyle(button);
  BootstrapButtons.setSmall(button);

  if (isEditable) {
    input.removeAttribute("disabled");
    button.removeAttribute("disabled");
  }

  return createThreeColumnLayout(label, input, button, 4, 4, 1);
};
