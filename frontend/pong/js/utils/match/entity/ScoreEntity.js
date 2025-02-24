import { CanvasEntity } from "./CanvasEntity";

export class ScoreEntity extends CanvasEntity {
  #pos;
  #score;

  constructor(x, y, color = "gray") {
    super(color);
    this.#pos = { x, y };
    this.#score = 0;
  }

  updateScore(score) {
    this.#score = score;
  }

  _draw(ctx) {
    ctx.textAlign = "center";
    ctx.font = "bold 30px sans-serif";
    ctx.fillText(this.#score, this.#pos.x, this.#pos.y);
  }
}
