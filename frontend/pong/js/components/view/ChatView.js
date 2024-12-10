import { View } from "../../core/View";

export class ChatView extends View {
  constructor(state = {}) {
    super(state);
    this._updateState({ history: [] });
    this.#connectWebSocket();
  }

  #connectWebSocket() {
    this._updateState({ status: "???" });

    // Create a new WebSocket connection
    const socket = new WebSocket("ws://localhost:8765");

    // Connection opened
    socket.addEventListener("open", (event) => {
      console.log("WebSocket connection established");
      socket.send("Hello, Server!");
      this._updateState({ status: "open" });
    });

    // Listen for messages from the server
    socket.addEventListener("message", (event) => {
      const message = event.data;
      console.log("Message from server:", message);
      const history = this._getState("history");
      this._updateState({
        history: [...history, { author: "Server", message }],
      });
    });

    // Connection closed
    socket.addEventListener("close", (event) => {
      console.log("WebSocket connection closed");
      this._updateState({ status: "closed" });
    });

    // Handle errors
    socket.addEventListener("error", (event) => {
      console.error("WebSocket error:", event);
      this._updateState({ status: "error" });
    });
  }

  _template() {
    const currentPath = this._getPath();
    const currentStatus = this._getState("status");
    const content = `<h1>path: ${currentPath}</h1> <h2>Status: ${currentStatus}</h2><h2>Welcome to 'Pong Chat'</h2>`;
    return content;
  }

  _afterRender() {
    const ul = document.createElement("ul");
    for (const { author, message } of this._getState("history")) {
      const li = document.createElement("li");
      li.innerText = `${author}: ${message}`;
      ul.appendChild(li);
    }
    this.appendChild(ul);
  }
}
