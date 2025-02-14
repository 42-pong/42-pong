import { LoginContainer } from "./auth/LoginContainer";
import { ChatBuddyListContainer } from "./chat/ChatBuddyListContainer";
import { ChatDmContainer } from "./chat/ChatDmContainer";
import { ChatGlobal } from "./chat/ChatGlobal";
import { ChatPanel } from "./chat/ChatPanel";
import { AddFriendButton } from "./friend/AddFriendButton";
import { GameStartPanel } from "./game/GameStartPanel";
import { MainNavbar } from "./navigation/MainNavbar";
import { TournamentContainer } from "./tournament/TournamentContainer";
import { TournamentEntrance } from "./tournament/TournamentEntrance";
import { TournamentFinished } from "./tournament/TournamentFinished";
import { TournamentOngoing } from "./tournament/TournamentOngoing";
import { TournamentProgress } from "./tournament/TournamentProgress";
import { TournamentProgressTransitionButton } from "./tournament/TournamentProgressTransitionButton";
import { TournamentStageTransitionButton } from "./tournament/TournamentStageTransitionButton";
import { TournamentStageTransitionButtonWithInput } from "./tournament/TournamentStageTransitionButtonWithInput";
import { TournamentWaiting } from "./tournament/TournamentWaiting";
import { BlockUserButton } from "./user/BlockUserButton";
import { UserListContainer } from "./user/UserListContainer";
import { UserListItem } from "./user/UserListItem";
import { UserProfile } from "./user/UserProfile";
import { UserProfileContainer } from "./user/UserProfileContainer";
import { ErrorContainer } from "./utils/ErrorContainer";
import { EventDispatchingButton } from "./utils/EventDispatchingButton";
import { LinkButton } from "./utils/LinkButton";
import { ListContainer } from "./utils/ListContainer";
import { ObservableInput } from "./utils/ObservableInput";
import { FriendsView } from "./views/FriendsView";
import { HomeView } from "./views/HomeView";
import { LoginView } from "./views/LoginView";
import { MainView } from "./views/MainView";
import { MyPageView } from "./views/MyPageView";
import { NotFoundView } from "./views/NotFoundView";
import { TournamentsView } from "./views/TournamentsView";
import { UsersView } from "./views/UsersView";

customElements.define("login-container", LoginContainer, {});
customElements.define(
  "chat-buddy-list-container",
  ChatBuddyListContainer,
  {},
);
customElements.define("chat-dm-container", ChatDmContainer, {});
customElements.define("chat-global", ChatGlobal, {});
customElements.define("chat-panel", ChatPanel, {});
customElements.define("add-friend-button", AddFriendButton, {});
customElements.define("game-start-panel", GameStartPanel, {});
customElements.define("main-navbar", MainNavbar, {});
customElements.define(
  "tournament-container",
  TournamentContainer,
  {},
);
customElements.define("tournament-entrance", TournamentEntrance, {});
customElements.define("tournament-finished", TournamentFinished, {});
customElements.define("tournament-ongoing", TournamentOngoing, {});
customElements.define("tournament-progress", TournamentProgress, {});
customElements.define(
  "tournament-progress-transition-button",
  TournamentProgressTransitionButton,
  {},
);
customElements.define(
  "tournament-stage-transition-button",
  TournamentStageTransitionButton,
  {},
);
customElements.define(
  "tournament-stage-transition-button-with-input",
  TournamentStageTransitionButtonWithInput,
  {},
);
customElements.define("tournament-waiting", TournamentWaiting, {});
customElements.define("block-user-button", BlockUserButton, {});
customElements.define("user-list-container", UserListContainer, {});
customElements.define("user-list-item", UserListItem, {});
customElements.define("user-profile", UserProfile, {});
customElements.define(
  "user-profile-container",
  UserProfileContainer,
  {},
);
customElements.define("error-container", ErrorContainer, {});
customElements.define(
  "event-dispatching-button",
  EventDispatchingButton,
  {},
);
customElements.define("link-button", LinkButton, {});
customElements.define("list-container", ListContainer, {});
customElements.define("observable-input", ObservableInput, {});
customElements.define("friends-view", FriendsView, {});
customElements.define("home-view", HomeView, {});
customElements.define("login-view", LoginView, {});
customElements.define("main-view", MainView, {});
customElements.define("my-page-view", MyPageView, {});
customElements.define("not-found-view", NotFoundView, {});
customElements.define("tournaments-view", TournamentsView, {});
customElements.define("users-view", UsersView, {});
