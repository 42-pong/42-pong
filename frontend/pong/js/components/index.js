import { MainNav } from "./navs/MainNav";
import { ChatView } from "./views/ChatView";
import { HomeView } from "./views/HomeView";
import { LoginView } from "./views/LoginView";

customElements.define("main-nav", MainNav, {});
customElements.define("chat-view", ChatView, {});
customElements.define("home-view", HomeView, {});
customElements.define("login-view", LoginView, {});
