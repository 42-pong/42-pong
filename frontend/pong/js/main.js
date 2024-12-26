import "./components";
import { homeRouter } from "./routers/homeRouter.js";

const app = document.getElementById("app");
const router = homeRouter(app);

router.update(window.location.pathname);
