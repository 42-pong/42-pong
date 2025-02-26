import { BootstrapBorders } from "../../bootstrap/utilities/borders";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { DataSubject } from "../../core/DataSubject";
import { WebSocketEnums } from "../../enums/WebSocketEnums";
import { UserSessionManager } from "../../session/UserSessionManager";
import { ChatMessage } from "../../utils/chat/ChatMessage";
import { isGroupChat } from "../../utils/chat/isGroupChat";
import { createElement } from "../../utils/elements/createElement";
import { createHorizontalSplitLayout } from "../../utils/elements/div/createHorizontalSplitLayout";
import { createVerticalSplitLayout } from "../../utils/elements/div/createVerticalSplitLayout";
import { setHeight } from "../../utils/elements/style/setHeight";
import { isValidId } from "../../utils/isValidId";
import { ChatPayload } from "../../websocket/payload/ChatPayload";
import { TournamentPayload } from "../../websocket/payload/TournamentPayload";
import { ChatContainer } from "../chat/ChatContainer";
import { MatchContainer } from "../match/MatchContainer";
import { TournamentParticipations } from "./TournamentParticipations";
import { TournamentStateContainer } from "./TournamentStateContainer";

export class TournamentProgress extends Component {
  #players;
  #tournamentStateContainer;
  #chatSubject;
  #groupChat;
  #listenGroupChat;
  #matchOverlay;
  #assignMatch;

  constructor(state = {}) {
    super({ isPlayingMatch: false, matchId: null, ...state });
    this.#chatSubject = new DataSubject({ messages: [] });
    this.#listenGroupChat = null;
    this.#matchOverlay = createElement("div");
  }

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setJustifyContentCenter(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSizing.setWidth100(this);
    BootstrapSizing.setHeight100(this);

    setHeight(this.#groupChat, "90%");
    BootstrapSpacing.setPadding(this.#groupChat, 3);
    BootstrapBorders.setBorder(this.#groupChat);
    BootstrapBorders.setRounded(this.#groupChat);
  }

  _onConnect() {
    const { tournamentId } = this._getState();

    this.#players = new TournamentParticipations({ tournamentId });

    this.#tournamentStateContainer = new TournamentStateContainer({
      tournamentId,
    });

    const myId = UserSessionManager.getInstance().myInfo.observe(
      ({ id }) => id,
    );
    const onMessageSubmit = (value) =>
      UserSessionManager.getInstance().webSocket.send(
        WebSocketEnums.Category.CHAT,
        ChatPayload.createGroupChat({
          fromId: myId,
          tournamentId,
          content: value,
        }),
      );

    this.#groupChat = new ChatContainer({
      chatSubject: this.#chatSubject,
      onMessageSubmit,
    });

    this.#listenGroupChat = (payload) => {
      const { type, data } = payload;
      const { to } = data;
      if (!(tournamentId === to && isGroupChat(type))) return;
      this.#chatSubject.updateData({
        newItem: new ChatMessage(type, data),
      });
    };

    UserSessionManager.getInstance().webSocket.attachHandler(
      WebSocketEnums.Category.CHAT,
      this.#listenGroupChat,
    );

    this.#clearMatchOverlay();
    this.#assignMatch = (payload) => {
      const { type, data } = payload;
      if (type !== WebSocketEnums.Tournament.Type.ASSIGNED) return;
      const { match_id: matchId } = data;
      if (isValidId(matchId)) this.#setMatchOverlay(matchId);
    };

    UserSessionManager.getInstance().webSocket.attachHandler(
      WebSocketEnums.Category.TOURNAMENT,
      this.#assignMatch,
    );

    this._attachEventListener(PongEvents.END_MATCH.type, (event) => {
      event.preventDefault();
      this.#clearMatchOverlay();
    });
  }

  _onDisconnect() {
    UserSessionManager.getInstance().webSocket.detachHandler(
      WebSocketEnums.Category.CHAT,
      this.#listenGroupChat,
    );
    this.#listenGroupChat = null;

    UserSessionManager.getInstance().webSocket.detachHandler(
      WebSocketEnums.Category.TOURNAMENT,
      this.#assignMatch,
    );
    this.assignMatch = null;

    const { tournamentId } = this._getState();

    UserSessionManager.getInstance().webSocket.send(
      WebSocketEnums.Category.TOURNAMENT,
      TournamentPayload.createLeave({
        tournamentId,
      }),
    );
  }

  _render() {
    const { tournamentId } = this._getState();

    // TODO: タイトル要素を作成する関数でまとめる
    const title = createElement("h1");
    title.textContent = `🏓 トーナメント #${tournamentId}`;
    BootstrapSpacing.setMargin(title, 5);

    const left = createHorizontalSplitLayout(
      this.#players,
      this.#tournamentStateContainer,
    );
    setHeight(this.#players, "20%");
    setHeight(this.#tournamentStateContainer, "60%");

    const right = this.#groupChat;

    const verticalSplit = createVerticalSplitLayout(
      left,
      right,
      7,
      4,
    );
    BootstrapSizing.setHeight75(verticalSplit);

    this.append(title, verticalSplit, this.#matchOverlay);
  }

  #clearMatchOverlay() {
    BootstrapDisplay.setNone(this.#matchOverlay);
    this.#matchOverlay.replaceChildren();
  }

  #setMatchOverlay(matchId) {
    this.#matchOverlay.append(new MatchContainer({ matchId }));
    BootstrapDisplay.unsetNone(this.#matchOverlay);
  }
}
