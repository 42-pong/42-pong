export class WebSocketWrapper {
  #socket;
  #handlers;

  constructor(url) {
    const socket = new WebSocket(url);
    this.#socket = socket;

    this.#handlers = {};

    socket.addEventListener("open", this.onOpen.bind(this));
    socket.addEventListener("close", this.onClose.bind(this));
    socket.addEventListener("error", this.onError.bind(this));
    socket.addEventListener("message", this.onMessage.bind(this));
  }

  get readyState() {
    return this.#socket.readyState;
  }

  send(category, payload) {
    if (this.#socket === null) return;
    this.#socket.send(JSON.stringify({ category, payload }));
  }

  // TODO: クローズコードと理由を指定できる形にする
  close() {
    if (this.#socket === null) return;
    this.#socket.close();
    this.#socket = null;
  }

  onOpen(event) {}

  onClose(event) {
    this.#socket = null;
  }

  onError(event) {
    this.#socket.close();
  }

  onMessage(event) {
    const { category, payload } = JSON.parse(event.data);
    const handler = this.#handlers[category];

    if (handler) handler(payload);
  }

  attachHandler(category, handler) {
    this.#handlers[category] = handler;
  }

  detachHandler(category) {
    delete this.#handlers[category];
  }
}
