import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { Component } from "../../core/Component";
import { createMatchCanvas } from "../../utils/match/createMatchCanvas";
import { CanvasEntity } from "../../utils/match/entity/CanvasEntity";

export class MatchRenderer extends Component {
  #canvas;
  #animationLoopId;

  constructor(state = {}) {
    super(state);
    this.#canvas = createMatchCanvas();
    this.#animationLoopId = null;
  }

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapFlex.setJustifyContentCenter(this);
  }

  _onDisconnect() {
    if (this.#animationLoopId) {
      cancelAnimationFrame(this.#animationLoopId);
      this.#animationLoopId = null;
    }
  }

  _render() {
    this.append(this.#canvas);
    this.#canvas.focus();

    const { entities } = this._getState();
    this.#animationLoopId = animate(this.#canvas, entities);
  }
}

const animate = (canvas, entities) => {
  const draw = () => {
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (const entity of Object.values(entities)) {
      if (entity instanceof CanvasEntity) entity.draw(ctx);
    }
    return requestAnimationFrame(draw);
  };
  return draw();
};
