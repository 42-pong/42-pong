import { CanvasEntity } from "./CanvasEntity";

export class BorderEntity extends CanvasEntity {
  #upperLeft;
  #width;
  #height;

  constructor(x, y, width, height, color = "gray") {
    super(color);
    this.#upperLeft = { x, y };
    this.#width = width;
    this.#height = height;
  }

  _draw(ctx) {
    // ctx.strokeStyle = 'black';
    // ctx.lineWidth = 5;
    ctx.strokeRect(
      this.#upperLeft.x,
      this.#upperLeft.y,
      this.#width,
      this.#height,
    );
  }
}
