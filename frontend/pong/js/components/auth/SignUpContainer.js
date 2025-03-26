import { BootstrapButtons } from "../../bootstrap/components/buttons";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { AuthConstants } from "../../constants/AuthConstants";
import { Endpoints } from "../../constants/Endpoints";
import { Paths } from "../../constants/Paths";
import { PongEvents } from "../../constants/PongEvents";
import { ApiMessage } from "../../constants/message/ApiMessage";
import { Component } from "../../core/Component";
import { MessageEnums } from "../../enums/MessageEnums";
import { setClassNames } from "../../utils/elements/setClassNames";
import { createTextElement } from "../../utils/elements/span/createTextElement";
import { getTextContent } from "../../utils/i18n/lang";

export class SignUpContainer extends Component {
  #title;
  #form;
  #loginError;
  #mailError;
  #passwordError;

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
    const title = createTextElement("Sign Up", 1);

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
    emailInput.pattern = `${AuthConstants.EMAIL_PATTERN}`;
    emailInput.setAttribute("autocomplete", "username");
    setClassNames(emailInput, "form-control");
    BootstrapSizing.setWidth50(emailInput);
    BootstrapSpacing.setMargin(emailInput);

    //メールのエラー文字
    this.#mailError = document.createElement("div");
    this.#mailError.className = "error-message";
    this.#mailError.style.color = "red";
    this.#mailError.style.display = "none"; //初期状態では非表示

    // パスワード入力フィールドを作成
    const passwordInput = document.createElement("input");
    passwordInput.type = "password";
    passwordInput.name = "password";
    passwordInput.placeholder = "Password";
    passwordInput.required = true;
    passwordInput.setAttribute("autocomplete", "new-password");
    setClassNames(passwordInput, "form-control");
    BootstrapSizing.setWidth50(passwordInput);
    BootstrapSpacing.setMargin(passwordInput);

    //パスワードのエラー文字
    this.#passwordError = document.createElement("div");
    this.#passwordError.className = "error-message";
    this.#passwordError.style.color = "red";
    this.#passwordError.style.display = "none"; //初期状態では非表示

    // サインインアップボタンを作成
    const submitButton = document.createElement("button");
    submitButton.type = "submit";
    submitButton.textContent = getTextContent("signup");
    BootstrapButtons.setPrimary(submitButton);
    BootstrapSizing.setWidth25(submitButton);

    form.append(
      this.#loginError,
      emailInput,
      this.#mailError,
      passwordInput,
      this.#passwordError,
      submitButton,
    );

    this.#title = title;
    this.#form = form;

    // サインインアップボタン
    // "api/accounts/"へfetchする
    this.#form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const email = this.#form.elements.email.value;
      const password = this.#form.elements.password.value;

      try {
        const response = await fetch(Endpoints.ACCOUNTS.href, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            email: email,
            password: password,
          }),
        });

        const { status, code } = await response.json();

        if (status !== "ok") {
          this.#form.reset();
          this.#handleStatusError(code);
        } else {
          this.#loginError.style.display = "none"; //エラーメッセージをデフォルトの非表示にする
          this.#mailError.style.display = "none";
          this.#passwordError.style.display = "none";

          // 成功メッセージを表示
          const successMessage = document.createElement("div");
          successMessage.className = "success-message";
          successMessage.textContent =
            "アカウントが正常に作成されました。ログインページにリダイレクトします...";
          successMessage.style.color = "green";
          this.#form.appendChild(successMessage);
          // 数秒後にログインページにリダイレクト
          setTimeout(() => {
            this.dispatchEvent(
              PongEvents.UPDATE_ROUTER.create(Paths.LOGIN),
            );
          }, 2000);
        }
      } catch (error) {
        console.error("ログインエラー:", error);
      }
    });
  }

  _render() {
    this.append(this.#title, this.#form);
  }

  #handleStatusError(code) {
    if (code && Array.isArray(code)) {
      const errorMessages = code
        .map((errorCode) => {
          const messageKey = MessageEnums.AccountsCode[errorCode];
          return messageKey
            ? ApiMessage.Accounts[messageKey]
            : `Unknown error: ${errorCode}`;
        })
        .join("<br>");
      this.#loginError.innerHTML = errorMessages;
      this.#loginError.style.display = "block";
      throw new Error(errorMessages);
    }
    this.#loginError.textContent = "An unknown error occurred";
    this.#loginError.style.display = "block";
    throw new Error("An unknown error occurred");
  }
}
