import { Component } from "../../core/Component";
import { createMatchCanvas } from "../../utils/match/createMatchCanvas";

export class MatchRenderer extends Component {
  #canvas;

  constructor(state = {}) {
    super(state);
    this.#canvas = createMatchCanvas();
  }

  _render() {
    this.append(this.#canvas);
    this.#canvas.focus();

    const { entities } = this._getState();
    animate(this.#canvas, entities);
  }
}

const animate = (canvas, entities) => {
  const draw = () => {
    const ctx = canvas.getContext("2d");
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (const entity of Object.values(entities)) {
      entity.draw(ctx);
    }
    requestAnimationFrame(draw);
  };
  draw();
};
