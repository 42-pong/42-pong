import { StyledButton } from "../../core/StyledButton";

export class EventDispatchingButton extends StyledButton {
  #customEvent;

  constructor(state = {}, attributes = {}, customEvent = null) {
    super(
      { textContent: "event-dispatching-button", ...state },
      { type: "button", ...attributes },
    );
    this.#customEvent = customEvent;
  }

  _onConnect() {
    if (this.#customEvent) {
      this._attachEventListener("click", (event) => {
        event.preventDefault();
        this.dispatchEvent(this.#customEvent.create());
      });
    }
  }
}
