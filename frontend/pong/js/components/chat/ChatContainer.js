import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Component } from "../../core/Component";
import { DataSubject } from "../../core/DataSubject";
import { ChatMessage } from "../../utils/chat/ChatMessage";
import { setHeight } from "../../utils/elements/style/setHeight";
import { ListContainer } from "../utils/ListContainer";
import { ChatInputForm } from "./ChatInputForm";
import { ChatMessageListItem } from "./ChatMessageListItem";

export class ChatContainer extends Component {
  #chatMessageList;
  #input;

  constructor(state = {}) {
    super({
      messages: [],
      chatSubject: null,
      onMessageSubmit: null,
      isError: false,
      ...state,
    });
  }

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapSpacing.setPadding(this);

    BootstrapDisplay.setFlex(this.#chatMessageList);
    BootstrapFlex.setFlexColumnReverse(this.#chatMessageList);
    setHeight(this.#chatMessageList, "90%");
    setHeight(this.#input, "10%");
  }

  _onConnect() {
    const { chatSubject, onMessageSubmit } = this._getState();

    if (!isValidProps(chatSubject, onMessageSubmit)) {
      Object.assign(this._state, { isError: true });
      return;
    }

    this.#input = new ChatInputForm({
      onMessageSubmit,
    });

    chatSubject.observe(({ messages }) => {
      this.#chatMessageList = new ListContainer({
        ListItem: ChatMessageListItem,
        items: messages,
        subject: chatSubject,
      });
    });
  }

  _render() {
    const { isError } = this._getState();
    if (isError) return;
    this.append(this.#chatMessageList, this.#input);
  }
}

const isValidChatMessages = (messages) =>
  Array.isArray(messages) &&
  messages.every((chat) => chat instanceof ChatMessage);

const isValidProps = (chatSubject, onMessageSubmit) =>
  chatSubject instanceof DataSubject &&
  typeof onMessageSubmit === "function" &&
  chatSubject.observe(({ messages }) =>
    isValidChatMessages(messages),
  );
