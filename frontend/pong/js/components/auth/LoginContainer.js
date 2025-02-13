import { Endpoints } from "../../constants/Endpoints";
import { Paths } from "../../constants/Paths";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { Cookie } from "../../utils/cookie/Cookie";
import { validateEmail } from "../../utils/validator/validateEmail";
import { validatePassword } from "../../utils/validator/validatePassword";

export class LoginContainer extends Component {
  #container;
  #title;
  #form;

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
    const signupButton = document.createElement("button");
    signupButton.type = "button";
    signupButton.textContent = "サインアップ";

    form.appendChild(emailInput);
    form.appendChild(passwordInput);
    form.appendChild(submitButton);
    form.appendChild(guestButton);
    form.appendChild(oauth2Button);
    form.appendChild(signupButton);

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
        const validateEmailResult = validateEmail(email);
        const validatePasswordResult = validatePassword(password);
        if (!validateEmailResult.valid)
          throw new Error(validateEmailResult.message);
        if (!validatePasswordResult.valid)
          throw new Error(validatePasswordResult.message);
        //todo
        //JWTエントポイント(api/token/)作成後に適用
      } catch (error) {
        //FEの画面に表示するエラーを実装
        // todo　APIのエラーメッセージハンドリング
        // not_exists : ユーザーが存在しません
        // incorrect_password : パスワードが間違っています
      }
    });
  }

  _render() {
    // コンテナにタイトルとフォームを追加
    this.#container.appendChild(this.#title);
    this.#container.appendChild(this.#form);

    // コンテナをカスタム要素に追加
    this.appendChild(this.#container);

    //todo
    //ログインページへ遷移した途端にJWT認証を行い、ホームページへリダイレクトする
    //cookieからJWTを取得する
    this.dispatchEvent(PongEvents.UPDATE_ROUTER.create(Paths.HOME));
  }
}
