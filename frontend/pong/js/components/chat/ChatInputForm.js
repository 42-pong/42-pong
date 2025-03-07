import { BootstrapButtons } from "../../bootstrap/components/buttons";
import { BootstrapBorders } from "../../bootstrap/utilities/borders";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Component } from "../../core/Component";
import { isValidGroupMessage } from "../../utils/chat/isValidGroupMessage";
import { createElement } from "../../utils/elements/createElement";
import { getTextContent } from "../../utils/i18n/lang";

export class ChatInputForm extends Component {
  #form;
  #input;
  #button;

  constructor(state = {}) {
    super({ onMessageSubmit: null, ...state });
  }

  _setStyle() {
    BootstrapButtons.setPrimary(this.#button);
    BootstrapDisplay.setFlex(this.#form);

    BootstrapSizing.setWidth75(this.#input);
    BootstrapSpacing.setPadding(this.#input);
    BootstrapSpacing.setMargin(this.#input);

    BootstrapSizing.setWidth25(this.#button);
    BootstrapSpacing.setPadding(this.#button);
    BootstrapSpacing.setMargin(this.#button);
    BootstrapButtons.setSmall(this.#button);
  }

  _onConnect() {
    this.#input = createElement(
      "input",
      {},
      { type: "text", placeholder: getTextContent("message") },
    );
    this.#button = createElement(
      "button",
      { textContent: getTextContent("send") },
      { type: "submit" },
    );
    this.#form = createElement("form");
    this.#form.append(this.#input, this.#button);

    const { onMessageSubmit } = this._getState();
    this._attachEventListener("submit", (event) => {
      event.preventDefault();
      const message = this.#input.value.trim();
      // TODO: グループメッセージの制限条件を確認
      if (!isValidGroupMessage(message)) {
        BootstrapBorders.setDanger(this.#input);
        return;
      }
      onMessageSubmit(message);
      BootstrapBorders.unsetDanger(this.#input);
      this.#input.value = "";
    });
  }

  _render() {
    this.append(this.#form);
  }
}
