import { Component } from "./Component";
import { HomePage } from "../components/page/HomePage";

export class App {
	#app;
	#routes;
	#PageComponent;
	#path;
	#page;

	// TODO: routes, router
	constructor(appNode) {
		this.#app = appNode;
		this.#routes = {
			"/": HomePage,
			"/about": HomePage,
		};
		const router = this.#router.bind(this, this.#routes, false);
		window.onpopstate = () => {
			router(window.location.pathname);
		};

		this.#router(this.#routes, false, "/");
	}

	#updatePage(path, PageComponent) {
		if (this.#PageComponent === PageComponent) {
			if (this.#path === path) return false;
			this.#path = path;
			this.#page._setState({ path });
		} else {
			const router = this.#router.bind(this, this.#routes, true);
			this.#PageComponent = PageComponent;
			this.#path = path;
			this.#page = new this.#PageComponent({ router }, { path });
			this.#refresh();
		}
		return true;
	}

	#router(routes, isUpdateHistory, location) {
		const path = location && routes[location] ? location : "/";
		const PageComponent = routes[path];
		const isUpdated = this.#updatePage(path, PageComponent);
		if (isUpdated && isUpdateHistory) window.history.pushState({}, "", path);
	}

	#refresh() {
		if (this.#app.firstChild) this.#app.removeChild(this.#app.firstChild);
		this.#app.appendChild(this.#page);
	}
}
