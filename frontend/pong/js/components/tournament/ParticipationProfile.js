import { getUser } from "../../api/users/getUser";
import { BootstrapText } from "../../bootstrap/utilities/text";
import { Component } from "../../core/Component";
import { createNameplate } from "../../utils/elements/div/createNameplate";

export class ParticipationProfile extends Component {
  static #DEFAULT_HEIGHT = "max(40px, 5vh)";

  constructor(state) {
    super({ participation: null, user: null, ...state });
  }

  _setStyle() {
    BootstrapText.setTextCenter(this);
  }

  _onConnect() {
    const { participation } = this._getState();
    if (!participation) return;

    const { displayName, userId } = participation;

    getUser(userId).then(({ user, error }) => {
      if (error) return;
      this._updateState({ user: { ...user, displayName } });
    });
  }

  _render() {
    const { user, height } = this._getState();
    this.append(
      createNameplate(
        user,
        height ?? ParticipationProfile.#DEFAULT_HEIGHT,
      ),
    );
  }
}
