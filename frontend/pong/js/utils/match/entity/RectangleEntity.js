import { CanvasEntity } from "./CanvasEntity";

export class RectangleEntity extends CanvasEntity {
  #upperLeft;
  #size;

  constructor(x, y, width, height, color = "gray") {
    super(color);
    this.#upperLeft = { x, y };
    this.#size = { width, height };
  }

  updateUpperLeft(newUpperLeft) {
    this.#upperLeft = newUpperLeft;
  }

  _draw(ctx) {
    ctx.fillRect(
      this.#upperLeft.x,
      this.#upperLeft.y,
      this.#size.width,
      this.#size.height,
    );
  }

  get upperLeft() {
    return this.#upperLeft;
  }

  get size() {
    return this.#size;
  }
}
