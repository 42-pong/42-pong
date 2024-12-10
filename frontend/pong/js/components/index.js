import { ChatView } from "./view/ChatView";
import { HomeView } from "./view/HomeView";
import { SignoutView } from "./view/SignoutView";

customElements.define("home-view", HomeView, {});
customElements.define("signout-view", SignoutView, {});
customElements.define("chat-view", ChatView, {});
