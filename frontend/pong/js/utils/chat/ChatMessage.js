export class ChatMessage {
  #type;
  #data;

  static Type = Object.freeze({
    DM: "DM",
    GROUP_CHAT: "GROUP_CHAT",
    GROUP_ANNOUNCEMENT: "GROUP_ANNOUNCEMENT",
  });

  constructor(type, data) {
    this.#type = type;
    this.#data = data;
  }

  get type() {
    return this.#type;
  }

  get data() {
    return this.#data;
  }
}
