import { AuthConstants } from "../../constants/AuthConstants";
import { Endpoints } from "../../constants/Endpoints";
import { Paths } from "../../constants/Paths";
import { PongEvents } from "../../constants/PongEvents";
import { ApiMessage } from "../../constants/message/ApiMessage";
import { Component } from "../../core/Component";
import { MessageEnums } from "../../enums/MessageEnums";

export class SignUpContainer extends Component {
  #container;
  #title;
  #form;
  #loginError;
  #mailError;
  #passwordError;

  _onConnect() {
    //コンテナ要素を作成
    const container = document.createElement("div");
    container.className = "form-container";

    //タイトル要素を作成
    const title = document.createElement("h1");
    title.textContent = "Sign Up";

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

    //パスワードのエラー文字
    this.#passwordError = document.createElement("div");
    this.#passwordError.className = "error-message";
    this.#passwordError.style.color = "red";
    this.#passwordError.style.display = "none"; //初期状態では非表示

    // サインインアップボタンを作成
    const submitButton = document.createElement("button");
    submitButton.type = "submit";
    submitButton.textContent = "サインアップ";

    form.append(
      this.#loginError,
      emailInput,
      this.#mailError,
      passwordInput,
      this.#passwordError,
      submitButton,
    );

    this.#container = container;
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
    // コンテナにタイトルとフォームを追加
    this.#container.append(this.#title, this.#form);
    // コンテナをカスタム要素に追加
    this.appendChild(this.#container);
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
