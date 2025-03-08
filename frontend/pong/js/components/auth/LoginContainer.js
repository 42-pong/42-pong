import { BootstrapButtons } from "../../bootstrap/components/buttons";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Endpoints } from "../../constants/Endpoints";
import { Paths } from "../../constants/Paths";
import { PongEvents } from "../../constants/PongEvents";
import { FrontendMessage } from "../../constants/message/FrontendMessage";
import { Component } from "../../core/Component";
import { MessageEnums } from "../../enums/MessageEnums";
import { setClassNames } from "../../utils/elements/setClassNames";
import { createTextElement } from "../../utils/elements/span/createTextElement";
import { getTextContent } from "../../utils/i18n/lang";
import { LinkButton } from "../utils/LinkButton";
import { OauthButton } from "./OauthButton";
import { SignUpButton } from "./SignUpButton";

export class LoginContainer extends Component {
  #title;
  #form;
  #loginError;

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setJustifyContentAround(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSpacing.setPadding(this);

    BootstrapDisplay.setFlex(this.#form);
    BootstrapFlex.setFlexColumn(this.#form);
    BootstrapFlex.setJustifyContentAround(this.#form);
    BootstrapFlex.setAlignItemsCenter(this.#form);
    BootstrapSizing.setWidth100(this.#form);
    BootstrapSizing.setHeight75(this.#form);
    BootstrapSpacing.setPadding(this.#form);
  }

  _onConnect() {
    //タイトル要素を作成
    const title = createTextElement("Pong 🏓", 1);

    //フォーム要素を作成
    const form = document.createElement("form");
    form.id = "login-form";

    //エラーメッセージ要素を作成
    this.#loginError = document.createElement("div");
    this.#loginError.className = "error-message";
    this.#loginError.style.color = "red";
    this.#loginError.style.display = "none"; //初期状態では非表示

    //メール入力フィールドを作成
    const emailInput = document.createElement("input");
    emailInput.type = "text";
    emailInput.name = "email";
    emailInput.placeholder = "E-mail";
    emailInput.required = true;
    emailInput.setAttribute("autocomplete", "username");
    setClassNames(emailInput, "form-control");
    BootstrapSizing.setWidth50(emailInput);
    BootstrapSpacing.setMargin(emailInput);

    // パスワード入力フィールドを作成
    const passwordInput = document.createElement("input");
    passwordInput.type = "password";
    passwordInput.name = "password";
    passwordInput.placeholder = "Password";
    passwordInput.required = true;
    passwordInput.setAttribute("autocomplete", "current-password");
    setClassNames(passwordInput, "form-control");
    BootstrapSizing.setWidth50(passwordInput);
    BootstrapSpacing.setMargin(passwordInput);

    // サインインボタンを作成
    const submitButton = document.createElement("button");
    submitButton.type = "submit";
    submitButton.textContent = getTextContent("signin");
    BootstrapButtons.setPrimary(submitButton);
    BootstrapSpacing.setMargin(submitButton);
    BootstrapSizing.setWidth25(submitButton);

    // ゲストボタン作成
    const guestButton = new LinkButton({
      textContent: getTextContent("guest"),
      pathname: Paths.HOME,
    });
    guestButton.setSecondary();
    BootstrapSpacing.setMargin(guestButton);
    BootstrapSizing.setWidth25(guestButton);

    // 42 OAuth2.0ボタン作成
    const oauthButton = new OauthButton();
    BootstrapSpacing.setMargin(oauthButton);
    BootstrapSizing.setWidth25(oauthButton);

    // サインアップボタン作成
    const signupButton = new SignUpButton();
    signupButton.setOutlinePrimary();
    BootstrapSpacing.setMargin(signupButton);
    BootstrapSizing.setWidth25(signupButton);

    form.append(
      this.#loginError,
      emailInput,
      passwordInput,
      submitButton,
      signupButton,
      oauthButton,
      guestButton,
    );

    this.#title = title;
    this.#form = form;

    // サインインボタン
    // "api/token/"へfetchする
    this.#form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const email = this.#form.elements.email.value;
      const password = this.#form.elements.password.value;
      try {
        const response = await fetch(Endpoints.LOGIN.href, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: email,
            password: password,
          }),
        });

        const { status, data, code } = await response.json();

        if (status !== "ok") {
          this.#form.reset();
          this.#loginError.textContent =
            FrontendMessage.Auth[MessageEnums.AuthCode.LOGIN_ERROR];
          this.#loginError.style.display = "block"; //エラーメッセージを表示する
          throw new Error(code);
        }
        this.#loginError.style.display = "none"; //エラーメッセージをデフォルトの非表示にする

        const { is_done_2fa: isDone2fa, qr_code: qrCode } = data;
        this.dispatchEvent(
          PongEvents.VERIFY_2FA.create({
            email,
            password,
            isDone2fa,
            qrCode,
          }),
        );
      } catch (error) {
        console.error("login error:", error);
      }
    });
  }

  _render() {
    this.append(this.#title, this.#form);
  }
}
