export class DataSubject {
  #data;
  #observers;

  constructor(data = {}) {
    this.#data = data;
    this.#observers = new Set();
  }

  init(data = {}) {
    this.#data = data;
    this.#notifyAll();
  }

  updateData(newData) {
    if (!newData) return;
    Object.assign(this.#data, newData);
    this.#notifyAll();
  }

  attach(observer) {
    const isAttachable = (observer) =>
      observer instanceof Function && !this.#observers.has(observer);
    if (!isAttachable(observer)) return;

    this.#observers.add(observer);
  }

  detach(observer) {
    if (!this.#observers.has(observer)) return;
    this.#observers.delete(observer);
  }

  #notify(observer) {
    observer(this.#data);
  }

  #notifyAll() {
    for (const observer of this.#observers) {
      this.#notify(observer);
    }
  }
}
