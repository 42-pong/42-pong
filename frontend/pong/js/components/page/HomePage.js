import { Component } from "../../core/Component";

export class HomePage extends Component {
	// TODO
	async loadStatus() {
		let status = "404";
		try {
			const response = await fetch("http://localhost:8000/api/health");
			const responseJson = await response.json();
			status = responseJson.status;
		} catch {
			status = "KO";
		}
		this._setState({ status });
	}

  // root
	_init() {
		const status = "???";
		this._setState({ status });
		this.loadStatus();
	}

	_template() {
		const currentStatus = this._getState("status");
		const currentPath = this._getState("path");

		let str = `<h1>path: ${currentPath}</h1> <h2>Status: ${currentStatus}</h2>`;
		const tabs = [
			{ path: "/", title: "HOME" },
			{ path: "/about", title: "ABOUT" },
		];
		for (const tab of tabs) {
			str += `<button class="btn" href="${tab.path}">${tab.title}</button>`;
		}
		return str;
	}

	_render() {
		this.innerHTML = this._template();
		this._afterRender();
	}

	_afterRender() {
		const router = this._getProps("router");
		const buttons = this.querySelectorAll(".btn");
		for (const button of buttons) {
			button.addEventListener("click", (event) => {
				const { target } = event;
				const href = target.getAttribute("href");
				router(href);
			});
		}
	}
}
