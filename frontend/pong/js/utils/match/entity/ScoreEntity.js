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

  _draw() {
    return;
  }

  get score() {
    return this.#score;
  }
}
