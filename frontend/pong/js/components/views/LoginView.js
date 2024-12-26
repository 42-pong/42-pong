import { View } from "../../core/View";


//ユーザーが入力するID、PWを保持する箱を入れる
//サイインボタンを押した後の処理
//フロントエンドのIDとPWバリデーション
//BEのエンドポイントにIDとPWを送った後のresponse処理

export class LoginView extends View {
	_render() {
	  const formHTML = `
	  <div class="form-container">
        <h1>Pong</h1>
        <form>
          <input type="text" name="email" placeholder="E-mail" required>
          <input type="password" name="password" placeholder="Password" required>
          <button type="submit">サインイン</button>
        </form>
      </div>
	  `;
	  this.innerHTML = formHTML;

	}
  }