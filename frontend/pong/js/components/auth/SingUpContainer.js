import { Component } from "../../core/Component";
import { Endpoints } from "../../constants/Endpoints";

export class SignUpContainer extends Component {
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

	  // パスワード入力フィールドを作成
	  const passwordInput = document.createElement("input");
	  passwordInput.type = "password";
	  passwordInput.name = "password";
	  passwordInput.placeholder = "Password";
	  passwordInput.required = true;

	  // サインインアップボタンを作成
	  const submitButton = document.createElement("button");
	  submitButton.type = "submit";
	  submitButton.textContent = "サインアップ";

	  form.append(
		this.#loginError,
		emailInput,
		passwordInput,
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
		  const { status, data: data} = await response.json();

		  if (status !== "ok") {
			this.#form.reset();
			this.#loginError.textContent =
			  FrontendMessage.Auth[MessageEnums.AuthCode.LOGIN_ERROR];
			this.#loginError.style.display = "block"; //エラーメッセージを表示する
			throw new Error(response.code);
		  }
		  this.#loginError.style.display = "none"; //エラーメッセージをデフォルトの非表示にする


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