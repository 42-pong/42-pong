import { Endpoints } from "../../constants/Endpoints";
import { Paths } from "../../constants/Paths";
import { FrontendMessage } from "../../constants/message/FrontendMessage";
import { Component } from "../../core/Component";
import { MessageEnums } from "../../enums/MessageEnums";
import { UserSessionManager } from "../../session/UserSessionManager";
import { SignUpButton } from "./SignUpButton";

export class LoginContainer extends Component {
  #container;
  #title;
  #form;
  #loginError;

  _onConnect() {
    //コンテナ要素を作成
    const container = document.createElement("div");
    container.className = "form-container";

    //タイトル要素を作成
    const title = document.createElement("h1");
    title.textContent = "Pong";

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

    // パスワード入力フィールドを作成
    const passwordInput = document.createElement("input");
    passwordInput.type = "password";
    passwordInput.name = "password";
    passwordInput.placeholder = "Password";
    passwordInput.required = true;

    // サインインボタンを作成
    const submitButton = document.createElement("button");
    submitButton.type = "submit";
    submitButton.textContent = "サインイン";

    // ゲストボタン作成
    const guestButton = document.createElement("button");
    guestButton.type = "button";
    guestButton.textContent = "ゲストとして";

    // 42 OAuth2.0ボタン作成
    const oauth2Button = document.createElement("button");
    oauth2Button.type = "button";
    oauth2Button.textContent = "42 OAuth 2.0";

    // サインアップボタン作成
    const signupButton = new SignUpButton();

    form.append(
      this.#loginError,
      emailInput,
      passwordInput,
      submitButton,
      guestButton,
      oauth2Button,
      signupButton,
    );

    this.#container = container;
    this.#title = title;
    this.#form = form;

    // サインインボタン
    // "api/token/"へfetchする
    this.#form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const email = this.#form.elements.email.value;
      const password = this.#form.elements.password.value;
      try {
        const response = await fetch(Endpoints.TOKEN.href, {
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

        const isVerified =
          await UserSessionManager.getInstance().signIn(data);
        if (isVerified)
          UserSessionManager.getInstance().redirect(Paths.HOME);
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

    //todo
    //ログインページへ遷移した途端にJWT認証を行い、ホームページへリダイレクトする
    //cookieからJWTを取得する
    //this.dispatchEvent(PongEvents.UPDATE_ROUTER.create(Paths.HOME));
  }
}
