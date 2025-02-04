import { BootstrapButtons } from "../../bootstrap/components/buttons";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Component } from "../../core/Component";
import { ObservableInput } from "../utils/ObservableInput";
import { TournamentStageTransitionButton } from "./TournamentStageTransitionButton";

export class TournamentStageTransitionButtonWithInput extends Component {
  #input;
  #button;

  constructor(
    state = {},
    inputAttributes = {},
    buttonState = {},
    buttonAttributes = {},
    tournamentStage = TournamentEnums.Stage.ENTRANCE,
  ) {
    super(state);
    this.#input = new ObservableInput({}, inputAttributes);
    this.#button = new TournamentStageTransitionButton(
      buttonState,
      buttonAttributes,
      tournamentStage,
    );
    this.#input.attach(
      this.#button.setTournamentId.bind(this.#button),
    );
  }

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapFlex.setJustifyContentAround(this);

    BootstrapSizing.setWidth50(this.#input);
    BootstrapSpacing.setPadding(this.#input);

    BootstrapSizing.setWidth50(this.#button);
    BootstrapSpacing.setPadding(this.#button);
  }

  _render() {
    this.appendChild(this.#input);
    this.appendChild(this.#button);
  }

  setPrimary() {
    this.#button.setPrimary();
  }

  setSecondary() {
    this.#button.setSecondary();
  }

  setOutlinePrimary() {
    this.#button.setOutlinePrimary();
  }

  setOutlineSecondary() {
    this.#button.setOutlineSecondary();
  }
}
