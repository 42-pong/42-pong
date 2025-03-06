import { CanvasEntity } from "./CanvasEntity";

export class ScoreHistoryEntity extends CanvasEntity {
  #pos;
  #label;
  #color;

  constructor(x, y, label, color = "red") {
    super(color);
    this.#pos = { x, y };
    this.#label = label;
    this.#color = color;
  }

  _draw(ctx) {
    ctx.beginPath();
    ctx.arc(this.#pos.x, this.#pos.y, 5, 0, 2 * Math.PI);
    ctx.fillStyle = this.#color;
    ctx.fill();

    ctx.fillStyle = "black";
    ctx.font = "14px Arial";
    ctx.textAlign = "center";
    ctx.textBaseline = "top";
    ctx.fillText(this.#label, this.#pos.x + 10, this.#pos.y - 10);
    return;
  }
}
