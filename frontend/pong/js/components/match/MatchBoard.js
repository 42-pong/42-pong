import { getMatch } from "../../api/matches/getMatch";
import { BootstrapBackground } from "../../bootstrap/utilities/background";
import { BootstrapBorders } from "../../bootstrap/utilities/borders";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Component } from "../../core/Component";
import { createEndFlexBox } from "../../utils/elements/div/createFlexBox";
import { createTextElement } from "../../utils/elements/span/createTextElement";
import { createMatchCanvas } from "../../utils/match/createMatchCanvas";
import { CanvasEntity } from "../../utils/match/entity/CanvasEntity";
import { createInitialMatchEntities } from "../../utils/match/entity/createInitialMatchEntities";
import { createScoreHistoryEntities } from "../../utils/match/entity/createScoreHistoryEntities";

export class MatchBoard extends Component {
  #isHidden;
  #canvas;
  #entities;
  #headerBar;

  constructor(state = {}) {
    super({ matchId: null, entities: [], ...state });
    this.#isHidden = true;
  }

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapFlex.setJustifyContentCenter(this);

    BootstrapBackground.setDarkSubtle(this.#headerBar);
    BootstrapBorders.setRounded(this.#headerBar);
    BootstrapSizing.setWidth100(this.#headerBar);
    BootstrapSpacing.setMargin(this.#headerBar);
  }

  _onConnect() {
    this.#canvas = createMatchCanvas();
    this.#entities = createInitialMatchEntities();

    const { createdAt } = this._getState();
    const createdTimestamp = createTextElement(
      new Date(createdAt).toLocaleString(),
      6,
    );

    const detailScores = createTextElement("ℹ️", 6);
    BootstrapSpacing.setMarginLeft(detailScores, 3);
    BootstrapSpacing.setMargin(detailScores, 1);
    this.#headerBar = createEndFlexBox(
      createdTimestamp,
      detailScores,
    );
    this.#headerBar.setAttribute("role", "button");

    this._attachEventListener("click", (event) => {
      event.preventDefault();
      this.#isHidden = !this.#isHidden;
      if (!this.#isHidden) this.reload();
      else this._updateState();
    });
  }

  _onDisconnect() {
    this.#canvas = null;
  }

  _render() {
    this.append(this.#headerBar);
    if (this.#isHidden) return;

    draw(this.#canvas, this.#entities);
    this.append(this.#canvas);
  }

  reload() {
    const { matchId } = this._getState();
    getMatch(matchId).then(({ match, error }) => {
      if (error) return;

      const ratio = this.#canvas.height / this.#canvas.width;
      this.#canvas.width = this.clientWidth;
      this.#canvas.height = this.clientWidth * ratio;

      const { players } = match;
      const scores = players.flatMap(({ scores }) => scores);
      this.#entities = createScoreHistoryEntities(
        this.#canvas.width,
        ...scores,
      );
      this._updateState();
    });
  }
}

const draw = (canvas, entities) => {
  const ctx = canvas.getContext("2d");
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  for (const entity of entities) {
    if (entity instanceof CanvasEntity) entity.draw(ctx);
  }
};
