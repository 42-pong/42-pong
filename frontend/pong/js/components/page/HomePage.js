import { Component } from "../../core/Component";

export class HomePage extends Component {
  // TODO
  async getStatus() {
    let status = "404";
    try {
      const response = await fetch("http://localhost:8000/api/health");
      const responseJson = await response.json();
      console.log(responseJson);
      status = responseJson.status;
    } catch {
      status = "KO";
    }
    this._setState({ status });
  }

  _init() {
    this._name = "home-page";
    const status = "???";
    this._setState({ status });
    this.getStatus();
  }

  _template() {
    const currentStatus = this._getState("status");
    return `<h1>Hello World</h1> <h2> Status: ${currentStatus}`;
  }
}
