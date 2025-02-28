export class CanvasEntity {
  #color;

  constructor(color) {
    this.#color = color;
  }

  _draw(ctx) {}

  draw(ctx) {
    ctx.fillStyle = this.#color;
    this._draw(ctx);
  }
}
