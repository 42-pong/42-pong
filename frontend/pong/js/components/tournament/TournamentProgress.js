import { BootstrapBorders } from "../../bootstrap/utilities/borders";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { DataSubject } from "../../core/DataSubject";
import { TournamentEnums } from "../../enums/TournamentEnums";
import { WebSocketEnums } from "../../enums/WebSocketEnums";
import { UserSessionManager } from "../../session/UserSessionManager";
import { ChatMessage } from "../../utils/chat/ChatMessage";
import { isGroupChat } from "../../utils/chat/isGroupChat";
import { createElement } from "../../utils/elements/createElement";
import { createHorizontalSplitLayout } from "../../utils/elements/div/createHorizontalSplitLayout";
import { createVerticalSplitLayout } from "../../utils/elements/div/createVerticalSplitLayout";
import { setHeight } from "../../utils/elements/style/setHeight";
import { ChatPayload } from "../../websocket/payload/ChatPayload";
import { TournamentPayload } from "../../websocket/payload/TournamentPayload";
import { ChatContainer } from "../chat/ChatContainer";
import { TournamentFinished } from "./TournamentFinished";
import { TournamentOngoing } from "./TournamentOngoing";
import { TournamentPlayers } from "./TournamentPlayers";
import { TournamentWaiting } from "./TournamentWaiting";

export class TournamentProgress extends Component {
  #players;
  #chatSubject;
  #groupChat;
  #listenGroupChat;

  constructor(state) {
    super({
      players: [],
      progress: TournamentEnums.Progress.WAITING,
      ...state,
    });
    this.#chatSubject = new DataSubject({ messages: [] });
    this.#listenGroupChat = null;
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

    const myId = UserSessionManager.myInfo.observe(({ id }) => id);
    this.#players = new TournamentPlayers({ tournamentId });
    const onMessageSubmit = (value) =>
      UserSessionManager.webSocket.send(
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

    this._attachEventListener(
      PongEvents.UPDATE_TOURNAMENT_PROGRESS.type,
      (event) => {
        const { progress } = event.detail;
        if (!(progress in TournamentEnums.Progress)) return;
        this._updateState({ progress });
      },
    );

    this.#listenGroupChat = (payload) => {
      const { type, data } = payload;
      const { to } = data;
      if (!(tournamentId === to && isGroupChat(type))) return;
      this.#chatSubject.updateData({
        newItem: new ChatMessage(type, data),
      });
    };

    UserSessionManager.webSocket.attachHandler(
      WebSocketEnums.Category.CHAT,
      this.#listenGroupChat,
    );
  }

  _onDisconnect() {
    UserSessionManager.webSocket.detachHandler(
      WebSocketEnums.Category.CHAT,
      this.#listenGroupChat,
    );
    this.#listenGroupChat = null;

    const { tournamentId } = this._getState();

    UserSessionManager.webSocket.send(
      WebSocketEnums.Category.TOURNAMENT,
      TournamentPayload.createLeave({
        tournamentId,
      }),
    );
  }

  _render() {
    const { progress, tournamentId } = this._getState();

    // TODO: タイトル要素を作成する関数でまとめる
    const title = createElement("h1");
    title.textContent = `🏓 トーナメント #${tournamentId}`;
    BootstrapSpacing.setMargin(title, 5);

    const currentProgressComponent = createCurrentProgressComponent(
      progress,
      tournamentId,
    );

    const left = createHorizontalSplitLayout(
      this.#players,
      currentProgressComponent,
    );
    setHeight(this.#players, "20%");
    setHeight(currentProgressComponent, "60%");

    const right = this.#groupChat;

    const verticalSplit = createVerticalSplitLayout(
      left,
      right,
      6,
      4,
    );
    BootstrapSizing.setHeight75(verticalSplit);

    this.append(title, verticalSplit);
  }
}

const createCurrentProgressComponent = (progress, tournamentId) => {
  switch (progress) {
    case TournamentEnums.Progress.WAITING:
      return new TournamentWaiting({ tournamentId });
    case TournamentEnums.Progress.ONGOING:
      return new TournamentOngoing({ tournamentId });
    case TournamentEnums.Progress.FINISHED:
      return new TournamentFinished({ tournamentId });
    default:
      return new TournamentWaiting({ tournamentId });
  }
};
