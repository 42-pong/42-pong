export class DataSubject {
  #data;
  #observers;

  constructor(data = {}) {
    this.#data = data;
    this.#observers = new Set();
  }

  init(data = {}) {
    this.#data = data;
    this.#notify();
  }

  updateData(newData) {
    if (!newData) return;
    Object.assign(this.#data, newData);
    this.#notify();
  }

  attach(observer) {
    const isAttachable = (observer) =>
      typeof observer === "function" &&
      !this.#observers.has(observer);
    if (!isAttachable(observer)) return;

    this.#observers.add(observer);
  }

  detach(observer) {
    if (!this.#observers.has(observer)) return;
    this.#observers.delete(observer);
  }

  observe(observer) {
    return observer(this.#data);
  }

  #notify() {
    for (const observer of this.#observers) {
      this.observe(observer);
    }
  }
}
