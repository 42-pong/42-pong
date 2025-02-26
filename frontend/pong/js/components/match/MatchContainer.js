import { BootstrapBadge } from "../../bootstrap/components/badge";
import { BootstrapBackground } from "../../bootstrap/utilities/background";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapPosition } from "../../bootstrap/utilities/position";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { MatchConstants } from "../../constants/MatchConstants";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { MatchEnums } from "../../enums/MatchEnums";
import { WebSocketEnums } from "../../enums/WebSocketEnums";
import { UserSessionManager } from "../../session/UserSessionManager";
import { customDelay } from "../../utils/customDelay";
import {
  createAroundFlexBox,
  createCenterFlexBox,
} from "../../utils/elements/div/createFlexBox";
import { createThreeColumnLayout } from "../../utils/elements/div/createThreeColumnLayout";
import { createTextElement } from "../../utils/elements/span/createTextElement";
import { isValidId } from "../../utils/isValidId";
import { createInitialMatchEntities } from "../../utils/match/entity/createInitialMatchEntities";
import { setEntities } from "../../utils/match/entity/setEntities";
import { EventDispatchingButton } from "../utils/EventDispatchingButton";
import { MatchRenderer } from "./MatchRenderer";
import { MatchRenderer3D } from "./MatchRenderer3D";

export class MatchContainer extends Component {
  #stage;
  #entities;
  #matchDataHandler;
  #keydownHandler;
  #renderer2d;
  #renderer3d;
  #toggle3d;
  #buttons;
  #centerPanel;

  #display1;
  #display2;
  #score1;
  #score2;
  #announcement;
  #statusBar;

  constructor(state = {}) {
    super({ is3d: true, matchId: null, ...state });
    this.#stage = MatchEnums.Stage.INIT;
    this.#entities = {};
  }

  _setStyle() {
    BootstrapPosition.setFixed(this);
    BootstrapPosition.setTop(this);
    BootstrapPosition.setStart(this);
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapFlex.setJustifyContentCenter(this);
    BootstrapBackground.setDarkSubtle(this);

    BootstrapSizing.setWidth100(this);
    BootstrapSizing.setViewportHeight100(this);
    BootstrapSpacing.setPadding(this, 4);

    BootstrapSpacing.setMargin(this.#statusBar, 4);
    BootstrapSizing.setWidth100(this.#statusBar);
    BootstrapSizing.setWidth100(this.#buttons);

    BootstrapSizing.setWidth100(this.#renderer2d);
    BootstrapSizing.setHeight100(this.#renderer2d);
    BootstrapSpacing.setMargin(this.#renderer2d, 4);

    BootstrapSizing.setWidth100(this.#renderer3d);
    BootstrapSizing.setHeight100(this.#renderer3d);
    BootstrapSpacing.setMargin(this.#renderer3d, 4);
  }

  _onConnect() {
    this.#entities = createInitialMatchEntities();
    this.#renderer2d = new MatchRenderer({
      entities: this.#entities,
    });
    this.#renderer3d = new MatchRenderer3D({
      entities: this.#entities,
    });

    this.#score1 = createTextElement(
      "0",
      2,
      BootstrapBadge.setSecondary,
    );
    this.#score2 = createTextElement(
      "0",
      2,
      BootstrapBadge.setSecondary,
    );
    this.#display1 = createTextElement("", 4);
    this.#display2 = createTextElement("", 4);
    this.#announcement = createTextElement(
      "",
      3,
      BootstrapBadge.setPrimary,
    );
    this.#centerPanel = createCenterFlexBox(this.#announcement);
    this.#statusBar = createThreeColumnLayout(
      createAroundFlexBox(this.#display1, this.#score1),
      this.#centerPanel,
      createAroundFlexBox(this.#score2, this.#display2),
      4,
      4,
      4,
    );

    const { is3d, matchId } = this._getState();

    this.#toggle3d = new EventDispatchingButton(
      {
        textContent: create3dConvertingMessage(is3d),
      },
      {},
      PongEvents.TOGGLE_3D,
    );
    this.#toggle3d.setPrimary();
    BootstrapSpacing.setMargin(this.#toggle3d);
    this.#buttons = createCenterFlexBox(this.#toggle3d);

    if (!matchId) {
      const backToHome = new EventDispatchingButton(
        { textContent: "ホームに戻る" },
        {},
        PongEvents.END_MATCH,
      );
      backToHome.setOutlinePrimary();
      BootstrapSpacing.setMargin(backToHome);

      this.#buttons.append(backToHome);
    }

    this._attachEventListener(PongEvents.TOGGLE_3D.type, () => {
      const { is3d } = this._getState();
      const newIs3d = !is3d;
      this.#toggle3d.setTextContent(
        create3dConvertingMessage(newIs3d),
      );
      this._updateState({ is3d: newIs3d });
    });

    const keydownHandler = (team) => (event) => {
      event.preventDefault();
      const { key } = event;

      const handler = keydownHandlers(team)[this.#stage];
      if (!handler) return;
      handler(key);
    };

    const dataHandlers = {
      [MatchEnums.Stage.INIT]: (data) => {
        setEntities.initStage(this.#entities, data);

        const { team, displayName1, displayName2 } = this.#entities;

        this.#keydownHandler = keydownHandler(team);
        document.addEventListener("keydown", this.#keydownHandler);

        this.#announcement.textContent = `Enter を押して${team ? "準備" : "スタート"}!`;

        this.#display1.textContent =
          displayName1 !== "" ? displayName1 : "LOCAL#1";
        this.#display2.textContent =
          displayName2 !== "" ? displayName2 : "LOCAL#2";

        this.#stage = MatchEnums.Stage.READY;
        this._updateState();
      },
      [MatchEnums.Stage.READY]: () => {
        this.#stage = MatchEnums.Stage.PLAY;
        this.#centerPanel.replaceChildren();
        this.#centerPanel.append(this.#buttons);
      },
      [MatchEnums.Stage.PLAY]: (data) => {
        setEntities.playStage(this.#entities, data);
        this.#score1.textContent = this.#entities.score1.score;
        this.#score2.textContent = this.#entities.score2.score;
      },
      [MatchEnums.Stage.END]: (data) => {
        setEntities.endStage(this.#entities, data);
        this.#stage = MatchEnums.Stage.END;
        this.#score1.textContent = this.#entities.score1.score;
        this.#score2.textContent = this.#entities.score2.score;
        const displayWonTeam =
          data.win === MatchEnums.Team.ONE
            ? this.#display1
            : this.#display2;
        displayWonTeam.textContent += " 🎉";

        customDelay(
          MatchConstants.AFTER_END_LOCAL_MATCH_REDIRECT_MS,
        ).then(() => {
          this.dispatchEvent(PongEvents.END_MATCH.create());
        });
      },
    };
    this.#matchDataHandler = (payload) => {
      const { stage, data } = payload;
      const handler = dataHandlers[stage];
      if (!handler) return;
      handler(data);
    };
    UserSessionManager.getInstance().webSocket.attachHandler(
      WebSocketEnums.Category.MATCH,
      this.#matchDataHandler,
    );

    sendInit(matchId);
  }

  _onDisconnect() {
    if (this.#stage !== MatchEnums.Stage.END)
      sendMatchData(MatchEnums.Stage.END, {});

    UserSessionManager.getInstance().webSocket.detachHandler(
      WebSocketEnums.Category.MATCH,
      this.#matchDataHandler,
    );

    document.removeEventListener("keydown", this.#keydownHandler);
  }

  _render() {
    if (this.#stage === MatchEnums.Stage.INIT) {
      this.append("...");
      return;
    }

    const { is3d } = this._getState();
    const renderer = is3d ? this.#renderer3d : this.#renderer2d;

    this.append(this.#statusBar, renderer);
  }
}

const sendMatchData = (stage, data) => {
  UserSessionManager.getInstance().webSocket.send(
    WebSocketEnums.Category.MATCH,
    { stage, data },
  );
};

const sendInit = (matchId) => {
  const data = isValidId(matchId)
    ? { mode: MatchEnums.Mode.REMOTE, match_id: matchId }
    : { mode: MatchEnums.Mode.LOCAL };

  sendMatchData(MatchEnums.Stage.INIT, data);
};

const getKeydownHandlerPlay = (team) => {
  switch (team) {
    case MatchEnums.Team.ONE:
      return (key) => {
        let move;
        switch (key) {
          case "ArrowUp":
          case "ArrowLeft":
            move = MatchEnums.Move.UP;
            break;
          case "ArrowDown":
          case "ArrowRight":
            move = MatchEnums.Move.DOWN;
            break;
          default:
            return;
        }
        sendMatchData(MatchEnums.Stage.PLAY, { team, move });
      };
    case MatchEnums.Team.TWO:
      return (key) => {
        let move;
        switch (key) {
          case "ArrowDown":
          case "ArrowLeft":
            move = MatchEnums.Move.DOWN;
            break;
          case "ArrowUp":
          case "ArrowRight":
            move = MatchEnums.Move.UP;
            break;
          default:
            return;
        }
        sendMatchData(MatchEnums.Stage.PLAY, { team, move });
      };
    default:
      break;
  }
  return (key) => {
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
  };
};

const keydownHandlers = (team) =>
  Object.freeze({
    [MatchEnums.Stage.READY]: (key) => {
      if (key === "Enter") sendMatchData(MatchEnums.Stage.READY, {});
    },
    [MatchEnums.Stage.PLAY]: getKeydownHandlerPlay(team),
  });

const create3dConvertingMessage = (is3d) =>
  `${is3d ? "2D" : "3D"} に切り替え`;
