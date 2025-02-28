import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { createElement } from "../../utils/elements/createElement";
import { EventDispatchingButton } from "../utils/EventDispatchingButton";

export class ChatDmContainer extends Component {
  #backToList;

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapSpacing.setPadding(this);
    this.#backToList.setSecondary();
  }

  _onConnect() {
    this.#backToList = new EventDispatchingButton(
      {
        textContent: "戻る",
      },
      {},
      PongEvents.TOGGLE_CHAT_USER_SELECTION,
    );
    this.#backToList.setSmall();
  }

  _render() {
    // TODO: dmPlaceHolder を実際のものに変更
    const dmPlaceHolder = createElement("span", {
      textContent: "[CHAT INTERFACE]",
    });
    this.append(this.#backToList, dmPlaceHolder);
  }
}
