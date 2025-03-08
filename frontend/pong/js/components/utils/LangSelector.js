import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { BootstrapText } from "../../bootstrap/utilities/text";
import { Component } from "../../core/Component";
import { createElement } from "../../utils/elements/createElement";
import { setClassNames } from "../../utils/elements/setClassNames";
import {
  getLang,
  getTextContent,
  setLang,
} from "../../utils/i18n/lang";

export class LangSelector extends Component {
  #select;

  static #langs = ["en", "jp", "fr", "zh", "es", "ko"];

  _setStyle() {
    setClassNames(this, "form-group-sm");
    BootstrapText.setTextCenter(this);
  }

  _onConnect() {
    const currentLang = getLang();
    this.#select = createElement("select", {});
    setClassNames(this.#select, "form-control-sm");
    for (const lang of LangSelector.#langs) {
      const option = createElement(
        "option",
        { textContent: getTextContent(lang) },
        { value: lang },
      );
      if (currentLang === lang) option.setAttribute("selected", "");
      this.#select.append(option);
    }

    this._attachEventListener("change", (event) => {
      event.preventDefault();

      const selectedLang = event.target.value;
      setLang(selectedLang);

      window.location.reload();
    });
  }

  _render() {
    const label = createElement("label", { textContent: "🌐" });
    BootstrapSpacing.setMargin(label);
    this.append(label, this.#select);
  }
}
