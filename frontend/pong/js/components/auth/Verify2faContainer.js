import { postTotp } from "../../api/utils/postTotp";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Endpoints } from "../../constants/Endpoints";
import { Paths } from "../../constants/Paths";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { UserSessionManager } from "../../session/UserSessionManager";
import { setClassNames } from "../../utils/elements/setClassNames";
import { setHeight } from "../../utils/elements/style/setHeight";
import { getTextContent } from "../../utils/i18n/lang";
import { EventDispatchingButton } from "../utils/EventDispatchingButton";

export class Verify2faContainer extends Component {
  #input;
  #button;

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setJustifyContentCenter(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSpacing.setPadding(this);
  }

  _onConnect() {
    this.#input = document.createElement("input", {
      type: "password",
    });
    this.#input.placeholder = "TOTP";
    this.#input.required = true;
    this.#input.setAttribute("autocomplete", "current-password");
    setClassNames(this.#input, "form-control");
    BootstrapSizing.setWidth50(this.#input);
    BootstrapSpacing.setMargin(this.#input);

    this.#button = new EventDispatchingButton(
      {
        textContent: getTextContent("send"),
      },
      {},
      PongEvents.VERIFY_TOTP,
    );
    this.#button.setPrimary();
    this.#button.setSmall();

    this._attachEventListener(
      PongEvents.VERIFY_TOTP.type,
      async (event) => {
        event.preventDefault();
        const { credentials } = this._getState();
        const { email, password } = credentials;

        const totp = this.#input.value;
        const { tokens, error } = await postTotp({
          email,
          password,
          totp,
        });
        if (error) {
          this.#onFail();
          return;
        }
        const isVerified =
          await UserSessionManager.getInstance().signIn(tokens);
        if (isVerified) this.#onSuccess();
        else this.#onFail();
      },
    );
  }

  _render() {
    const { credentials } = this._getState();
    const { email, password, isDone2fa, qrCode } = credentials;

    if (!(email && password)) this.#onFail();

    if (!isDone2fa) {
      const qrCodeImg = createQrCodeImg(
        qrCode,
        this.#onFail.bind(this),
      );
      this.append(qrCodeImg);
    }
    this.append(this.#input, this.#button);
  }

  #onFail() {
    UserSessionManager.getInstance().redirect(Paths.LOGIN);
  }

  #onSuccess() {
    UserSessionManager.getInstance().redirect(Paths.HOME);
  }
}

const createQrCodeImg = (pathname, onFail = null) => {
  const image = new Image();
  image.src = Endpoints.create(pathname).href;
  image.alt = "qrcode";
  image.onerror = () => {
    image.onerror = null;
    console.warn("qrcode not found!");
    if (onFail) onFail();
  };
  setHeight(image, "30vh");
  return image;
};
