import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { MatchEnums } from "../../enums/MatchEnums";
import { WebSocketEnums } from "../../enums/WebSocketEnums";
import { UserSessionManager } from "../../session/UserSessionManager";
import { customDelay } from "../../utils/customDelay";
import { createInitialMatchEntities } from "../../utils/match/entity/createInitialMatchEntities";
import { setEntities } from "../../utils/match/entity/setEntities";
import { MatchRenderer } from "./MatchRenderer";

export class MatchContainer extends Component {
  #entities;
  #dataHandlers;
  #matchDataHandler;
  #matchRenderer;

  constructor(state = {}) {
    super({
      stage: MatchEnums.Stage.INIT,
      ...state,
    });
    this.#entities = {};
    this.#dataHandlers = {
      [MatchEnums.Stage.INIT]: (data) => {
        setEntities.initStage(this.#entities, data);
        this._updateState({ stage: MatchEnums.Stage.READY });
      },
      [MatchEnums.Stage.READY]: (data) => {
        this._updateState({ stage: MatchEnums.Stage.PLAY });
      },
      [MatchEnums.Stage.PLAY]: (data) => {
        setEntities.playStage(this.#entities, data);
      },
      [MatchEnums.Stage.END]: (data) => {
        this._updateState({ stage: MatchEnums.Stage.END });
      },
    };
  }

  _onConnect() {
    this.#entities = createInitialMatchEntities();

    this.#matchRenderer = new MatchRenderer({
      entities: this.#entities,
    });

    this._attachEventListener("keydown", (event) => {
      const { key } = event;
      const { stage } = this._getState();

      const handler = keydownHandlers[stage];
      if (!handler) return;

      handler(key);
    });

    this.#matchDataHandler = (payload) => {
      const { stage, data } = payload;
      const handler = this.#dataHandlers[stage];
      if (!handler) return;
      handler(data);
    };
    UserSessionManager.getInstance().webSocket.attachHandler(
      WebSocketEnums.Category.MATCH,
      this.#matchDataHandler,
    );

    sendMatchData(MatchEnums.Stage.INIT, {
      mode: MatchEnums.Mode.LOCAL,
    });
  }

  _onDisconnect() {
    const { stage } = this._getState();
    if (stage !== MatchEnums.Stage.END)
      sendMatchData(MatchEnums.Stage.END, {});

    UserSessionManager.getInstance().webSocket.detachHandler(
      WebSocketEnums.Category.MATCH,
      this.#matchDataHandler,
    );
  }

  _render() {
    const { stage } = this._getState();

    switch (stage) {
      case MatchEnums.Stage.INIT:
        this.renderInit();
        break;
      case MatchEnums.Stage.READY:
        this.renderReady();
        break;
      case MatchEnums.Stage.PLAY:
        this.renderPlay();
        break;
      case MatchEnums.Stage.END:
        this.renderEnd();
        break;
    }
  }

  renderInit() {
    this.append("...");
  }

  renderReady() {
    this.append(this.#matchRenderer);
  }

  renderPlay() {
    this.append(this.#matchRenderer);
  }

  renderEnd() {
    this.append(this.#matchRenderer);
    customDelay(3000).then(() => {
      this.dispatchEvent(PongEvents.END_MATCH.create());
    });
  }
}

const sendMatchData = (stage, data) => {
  UserSessionManager.getInstance().webSocket.send(
    WebSocketEnums.Category.MATCH,
    { stage, data },
  );
};

const keydownHandlers = {
  [MatchEnums.Stage.READY]: (key) => {
    if (key === "Enter") sendMatchData(MatchEnums.Stage.READY, {});
  },
  [MatchEnums.Stage.PLAY]: (key) => {
    const data = {};
    switch (key) {
      case "ArrowUp":
        data.team = MatchEnums.Team.TWO;
        data.move = MatchEnums.Move.UP;
        break;
      case "ArrowDown":
        data.team = MatchEnums.Team.TWO;
        data.move = MatchEnums.Move.DOWN;
        break;
      case "w":
      case "W":
        data.team = MatchEnums.Team.ONE;
        data.move = MatchEnums.Move.UP;
        break;
      case "s":
      case "S":
        data.team = MatchEnums.Team.ONE;
        data.move = MatchEnums.Move.DOWN;
        break;
      default:
        return;
    }
    sendMatchData(MatchEnums.Stage.PLAY, data);
  },
};
