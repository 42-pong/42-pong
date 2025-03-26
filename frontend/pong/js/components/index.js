import { LoginContainer } from "./auth/LoginContainer";
import { OauthButton } from "./auth/OauthButton";
import { SignInButton } from "./auth/SignInButton";
import { SignOutButton } from "./auth/SignOutButton";
import { SignUpButton } from "./auth/SignUpButton";
import { SignUpContainer } from "./auth/SignUpContainer";
import { Verify2faContainer } from "./auth/Verify2faContainer";
import { BlockListContainer } from "./block/BlockListContainer";
import { BlockListItem } from "./block/BlockListItem";
import { BlockUserButton } from "./block/BlockUserButton";
import { UnblockUserButton } from "./block/UnblockUserButton";
import { ChatBuddyListContainer } from "./chat/ChatBuddyListContainer";
import { ChatContainer } from "./chat/ChatContainer";
import { ChatDmContainer } from "./chat/ChatDmContainer";
import { ChatGlobal } from "./chat/ChatGlobal";
import { ChatInputForm } from "./chat/ChatInputForm";
import { ChatMessageListItem } from "./chat/ChatMessageListItem";
import { ChatPanel } from "./chat/ChatPanel";
import { DashboardContainer } from "./dashboard/DashboardContainer";
import { DashboardStats } from "./dashboard/DashboardStats";
import { AddFriendButton } from "./friend/AddFriendButton";
import { RemoveFriendButton } from "./friend/RemoveFriendButton";
import { GameStartPanel } from "./game/GameStartPanel";
import { MatchBoard } from "./match/MatchBoard";
import { MatchCard } from "./match/MatchCard";
import { MatchContainer } from "./match/MatchContainer";
import { MatchRenderer } from "./match/MatchRenderer";
import { MatchRenderer3D } from "./match/MatchRenderer3D";
import { PlayerProfile } from "./match/PlayerProfile";
import { MainNavbar } from "./navigation/MainNavbar";
import { ParticipationProfile } from "./tournament/ParticipationProfile";
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
import { MyInfoAvatar } from "./user/MyInfoAvatar";
import { MyInfoContainer } from "./user/MyInfoContainer";
import { UserListContainer } from "./user/UserListContainer";
import { UserListItem } from "./user/UserListItem";
import { UserProfile } from "./user/UserProfile";
import { UserProfileContainer } from "./user/UserProfileContainer";
import { UserProfileHeader } from "./user/UserProfileHeader";
import { ErrorContainer } from "./utils/ErrorContainer";
import { EventDispatchingButton } from "./utils/EventDispatchingButton";
import { LangSelector } from "./utils/LangSelector";
import { LinkButton } from "./utils/LinkButton";
import { ListContainer } from "./utils/ListContainer";
import { ObservableInput } from "./utils/ObservableInput";
import { DashboardView } from "./views/DashboardView";
import { ErrorView } from "./views/ErrorView";
import { FriendsView } from "./views/FriendsView";
import { HomeView } from "./views/HomeView";
import { LoadingView } from "./views/LoadingView";
import { LoginView } from "./views/LoginView";
import { MainView } from "./views/MainView";
import { MyPageView } from "./views/MyPageView";
import { NotFoundView } from "./views/NotFoundView";
import { SignUpView } from "./views/SignUpView";
import { TournamentsView } from "./views/TournamentsView";
import { UsersView } from "./views/UsersView";

customElements.define("login-container", LoginContainer, {});
customElements.define("oauth-button", OauthButton, {});
customElements.define("sign-in-button", SignInButton, {});
customElements.define("sign-out-button", SignOutButton, {});
customElements.define("sign-up-button", SignUpButton, {});
customElements.define("sign-up-container", SignUpContainer, {});
customElements.define("verify-2fa-container", Verify2faContainer, {});
customElements.define("block-list-container", BlockListContainer, {});
customElements.define("block-list-item", BlockListItem, {});
customElements.define("block-user-button", BlockUserButton, {});
customElements.define("unblock-user-button", UnblockUserButton, {});
customElements.define(
  "chat-buddy-list-container",
  ChatBuddyListContainer,
  {},
);
customElements.define("chat-container", ChatContainer, {});
customElements.define("chat-dm-container", ChatDmContainer, {});
customElements.define("chat-global", ChatGlobal, {});
customElements.define("chat-input-form", ChatInputForm, {});
customElements.define(
  "chat-message-list-item",
  ChatMessageListItem,
  {},
);
customElements.define("chat-panel", ChatPanel, {});
customElements.define("dashboard-container", DashboardContainer, {});
customElements.define("dashboard-stats", DashboardStats, {});
customElements.define("add-friend-button", AddFriendButton, {});
customElements.define("remove-friend-button", RemoveFriendButton, {});
customElements.define("game-start-panel", GameStartPanel, {});
customElements.define("match-board", MatchBoard, {});
customElements.define("match-card", MatchCard, {});
customElements.define("match-container", MatchContainer, {});
customElements.define("match-renderer", MatchRenderer, {});
customElements.define("match-renderer-3d", MatchRenderer3D, {});
customElements.define("player-profile", PlayerProfile, {});
customElements.define("main-navbar", MainNavbar, {});
customElements.define(
  "participation-profile",
  ParticipationProfile,
  {},
);
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
customElements.define("my-info-avatar", MyInfoAvatar, {});
customElements.define("my-info-container", MyInfoContainer, {});
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
customElements.define("lang-selector", LangSelector, {});
customElements.define("link-button", LinkButton, {});
customElements.define("list-container", ListContainer, {});
customElements.define("observable-input", ObservableInput, {});
customElements.define("dashboard-view", DashboardView, {});
customElements.define("error-view", ErrorView, {});
customElements.define("friends-view", FriendsView, {});
customElements.define("home-view", HomeView, {});
customElements.define("loading-view", LoadingView, {});
customElements.define("login-view", LoginView, {});
customElements.define("sign-up-view", SignUpView, {});
customElements.define("main-view", MainView, {});
customElements.define("my-page-view", MyPageView, {});
customElements.define("not-found-view", NotFoundView, {});
customElements.define("tournaments-view", TournamentsView, {});
customElements.define("users-view", UsersView, {});
