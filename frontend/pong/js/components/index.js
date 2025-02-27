import { LoginContainer } from "./auth/LoginContainer";
import { SignInButton } from "./auth/SignInButton";
import { SignOutButton } from "./auth/SignOutButton";
import { ChatBuddyListContainer } from "./chat/ChatBuddyListContainer";
import { ChatContainer } from "./chat/ChatContainer";
import { ChatDmContainer } from "./chat/ChatDmContainer";
import { ChatGlobal } from "./chat/ChatGlobal";
import { ChatInputForm } from "./chat/ChatInputForm";
import { ChatMessageListItem } from "./chat/ChatMessageListItem";
import { ChatPanel } from "./chat/ChatPanel";
import { AddFriendButton } from "./friend/AddFriendButton";
import { GameStartPanel } from "./game/GameStartPanel";
import { MainNavbar } from "./navigation/MainNavbar";
import { MatchCard } from "./tournament/MatchCard";
import { ParticipationProfile } from "./tournament/ParticipationProfile";
import { PlayerProfile } from "./tournament/PlayerProfile";
import { RoundCard } from "./tournament/RoundCard";
import { TournamentContainer } from "./tournament/TournamentContainer";
import { TournamentEntrance } from "./tournament/TournamentEntrance";
import { TournamentFinished } from "./tournament/TournamentFinished";
import { TournamentJoinButton } from "./tournament/TournamentJoinButton";
import { TournamentLeaveButton } from "./tournament/TournamentLeaveButton";
import { TournamentOngoing } from "./tournament/TournamentOngoing";
import { TournamentParticipations } from "./tournament/TournamentParticipations";
import { TournamentProgress } from "./tournament/TournamentProgress";
import { TournamentScoreboard } from "./tournament/TournamentScoreboard";
import { TournamentStateContainer } from "./tournament/TournamentStateContainer";
import { TournamentWaiting } from "./tournament/TournamentWaiting";
import { BlockUserButton } from "./user/BlockUserButton";
import { UserListContainer } from "./user/UserListContainer";
import { UserListItem } from "./user/UserListItem";
import { UserProfile } from "./user/UserProfile";
import { UserProfileContainer } from "./user/UserProfileContainer";
import { UserProfileHeader } from "./user/UserProfileHeader";
import { ErrorContainer } from "./utils/ErrorContainer";
import { EventDispatchingButton } from "./utils/EventDispatchingButton";
import { LinkButton } from "./utils/LinkButton";
import { ListContainer } from "./utils/ListContainer";
import { ObservableInput } from "./utils/ObservableInput";
import { ErrorView } from "./views/ErrorView";
import { FriendsView } from "./views/FriendsView";
import { HomeView } from "./views/HomeView";
import { LoadingView } from "./views/LoadingView";
import { LoginView } from "./views/LoginView";
import { MainView } from "./views/MainView";
import { MyPageView } from "./views/MyPageView";
import { NotFoundView } from "./views/NotFoundView";
import { TournamentsView } from "./views/TournamentsView";
import { UsersView } from "./views/UsersView";

customElements.define("login-container", LoginContainer, {});
customElements.define("sign-in-button", SignInButton, {});
customElements.define("sign-out-button", SignOutButton, {});
customElements.define("chat-container", ChatContainer, {});
customElements.define(
  "chat-buddy-list-container",
  ChatBuddyListContainer,
  {},
);
customElements.define("chat-dm-container", ChatDmContainer, {});
customElements.define("chat-global", ChatGlobal, {});
customElements.define("chat-input-form", ChatInputForm, {});
customElements.define(
  "chat-message-list-item",
  ChatMessageListItem,
  {},
);
customElements.define("chat-panel", ChatPanel, {});
customElements.define("add-friend-button", AddFriendButton, {});
customElements.define("game-start-panel", GameStartPanel, {});
customElements.define("main-navbar", MainNavbar, {});
customElements.define("match-card", MatchCard, {});
customElements.define(
  "participation-profile",
  ParticipationProfile,
  {},
);
customElements.define("player-profile", PlayerProfile, {});
customElements.define("round-card", RoundCard, {});
customElements.define(
  "tournament-container",
  TournamentContainer,
  {},
);
customElements.define("tournament-entrance", TournamentEntrance, {});
customElements.define("tournament-finished", TournamentFinished, {});
customElements.define(
  "tournament-join-button",
  TournamentJoinButton,
  {},
);
customElements.define(
  "tournament-leave-button",
  TournamentLeaveButton,
  {},
);
customElements.define("tournament-ongoing", TournamentOngoing, {});
customElements.define(
  "tournament-players",
  TournamentParticipations,
  {},
);
customElements.define("tournament-progress", TournamentProgress, {});
customElements.define(
  "tournament-scoreboard",
  TournamentScoreboard,
  {},
);
customElements.define(
  "tournament-state-container",
  TournamentStateContainer,
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
customElements.define("user-profile-header", UserProfileHeader, {});
customElements.define("error-container", ErrorContainer, {});
customElements.define(
  "event-dispatching-button",
  EventDispatchingButton,
  {},
);
customElements.define("link-button", LinkButton, {});
customElements.define("list-container", ListContainer, {});
customElements.define("observable-input", ObservableInput, {});
customElements.define("error-view", ErrorView, {});
customElements.define("friends-view", FriendsView, {});
customElements.define("home-view", HomeView, {});
customElements.define("loading-view", LoadingView, {});
customElements.define("login-view", LoginView, {});
customElements.define("main-view", MainView, {});
customElements.define("my-page-view", MyPageView, {});
customElements.define("not-found-view", NotFoundView, {});
customElements.define("tournaments-view", TournamentsView, {});
customElements.define("users-view", UsersView, {});
