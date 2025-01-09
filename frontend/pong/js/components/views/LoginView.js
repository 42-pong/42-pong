import { View } from "../../core/View";

//ユーザーが入力するID、PWを保持する箱を入れる
//サイインボタンを押した後の処理
//フロントエンドのIDとPWバリデーション
//BEのエンドポイントにIDとPWを送った後のresponse処理

export class LoginView extends View {
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
  }

  _render() {
    // コンテナにタイトルとフォームを追加
    this.#container.appendChild(this.#title);
    this.#container.appendChild(this.#form);

    // コンテナをカスタム要素に追加
    this.appendChild(this.#container);

    // TODO 各ボタンの条件分岐でAPIエンドポイントにフェッチ(以下からのコードはBEのエントポイントと連携するため、レビューしない)
    // "api/signin/"　へfetchする
    this.#form.addEventListener("submit", async (event) => {
      event.preventDefault();
      const email = this.#form.elements.email.value;
      const password = this.#form.elements.password.value;
      console.log("Email", email);
      console.log("Password", password);

      try {
        const response = await fetch(
          "http://localhost:8000/api/signin/",
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
          },
        );

        if (!response.ok) {
          throw new Error("Network response was not ok");
        }

        const data = await response.json();
        console.log("Success:", data);
        // ここで成功時の処理を追加できます
      } catch (error) {
        console.error("Error:", error);
        // ここでエラーハンドリングを追加できます
      }
    });

    // "api/oauth2/authorize/”　へfetchする
    this.#form.addEventListener("42oauth", async (event) => {
      event.preventDefault();
      try {
        const response = await fetch(
          "http://localhost:8000/api/oauth2/authorize/",
          {
            method: "GET",
          },
        );
        if (!response.ok) {
          throw new Error("Oauth2 response was not ok");
        }

        const data = await response.json();
        console.log("Success", data);
      } catch (error) {
        console.error("Error:", error);
      }
    });
  }
}
