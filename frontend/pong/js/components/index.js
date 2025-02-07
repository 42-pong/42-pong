import { LoginContainer } from "./auth/LoginContainer";
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
import { LinkButton } from "./utils/LinkButton";
import { ObservableInput } from "./utils/ObservableInput";
import { ChatView } from "./views/ChatView";
import { FriendsView } from "./views/FriendsView";
import { HomeView } from "./views/HomeView";
import { LoginView } from "./views/LoginView";
import { MainView } from "./views/MainView";
import { MyPageView } from "./views/MyPageView";
import { NotFoundView } from "./views/NotFoundView";
import { TournamentsView } from "./views/TournamentsView";
import { UsersView } from "./views/UsersView";

customElements.define("login-container", LoginContainer, {});
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
customElements.define("link-button", LinkButton, {});
customElements.define("observable-input", ObservableInput, {});
customElements.define("chat-view", ChatView, {});
customElements.define("friends-view", FriendsView, {});
customElements.define("home-view", HomeView, {});
customElements.define("login-view", LoginView, {});
customElements.define("main-view", MainView, {});
customElements.define("my-page-view", MyPageView, {});
customElements.define("not-found-view", NotFoundView, {});
customElements.define("tournaments-view", TournamentsView, {});
customElements.define("users-view", UsersView, {});
