import { View } from "../../core/View";

export class LoginView extends View {
  #form;
  #email;
  #password;

  _onConnect() {
    const formHTML = `
      <style>
        .form-button {
          display: block;
          margin: 10px 0;
        }
      </style>
      <form>
        <label for="Email">ID:</label>
        <input type="text" name="Email" placeholder="E-mail">
        <br>
        <label for="Password">PW:</label>
        <input type="password" name="Password" placeholder="Password">
        <br>
        <button type="submit" class="form-button">サイイン</button>
        <button id="guestLogin" class="form-button">ゲストとして</button>
        <button id="oauth2.0" class="form-button">42 OAuth2.0</button>
        <button id="singUp" class="form-button">サインアップ</button>
      </form>
    `;

    //HTMLをDOMに挿入
    this.innerHTML = formHTML;
    // フォーム要素を取得
    this.#form = this.querySelector('form');
    this.#email = this.querySelector('input[name="Email"]');
    this.#password = this.querySelector('input[name="Password"]');

    this.#form.addEventListener('submit', (event) => {
      event.preventDefault();
      const email = this.#email.value;
      const password = this.#password.value;
      console.log('Email:', email);
      console.log('Password:', password);
      debugger;
      // ここでメールアドレスとパスワードを送信する処理を追加できます
    });
  }

  _render() {
    this.appendChild(this.#form);
  }
}
