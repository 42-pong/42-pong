import { BootstrapButtons } from "../bootstrap/components/buttons";
import { BootstrapSizing } from "../bootstrap/utilities/sizing";
import { createButton } from "../utils/elements/button/createButton";
import { Component } from "./Component";

export class StyledButton extends Component {
  _button;

  constructor(state = {}, attributes = {}) {
    super({ textContent: "StyledButton", ...state });
    this._button = createButton(this._getState(), attributes);
    BootstrapSizing.setWidth100(this._button);
  }

  _render() {
    this.append(this._button);
  }

  setTextContent(textContent) {
    this._button.textContent = textContent;
  }

  setDisabled() {
    this._button.setAttribute("disabled", "");
  }

  unsetDisabled() {
    this._button.removeAttribute("disabled");
  }

  setPrimary() {
    BootstrapButtons.setPrimary(this._button);
  }

  setSecondary() {
    BootstrapButtons.setSecondary(this._button);
  }

  setSuccess() {
    BootstrapButtons.setSuccess(this._button);
  }

  setDanger() {
    BootstrapButtons.setDanger(this._button);
  }

  setOutlinePrimary() {
    BootstrapButtons.setOutlinePrimary(this._button);
  }

  setOutlineSecondary() {
    BootstrapButtons.setOutlineSecondary(this._button);
  }

  setOutlineDanger() {
    BootstrapButtons.setOutlineDanger(this._button);
  }

  setSmall() {
    BootstrapButtons.setSmall(this._button);
  }
}
