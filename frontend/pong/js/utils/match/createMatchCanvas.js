import { MatchConstants } from "../../constants/MatchConstants";
import { createElement } from "../elements/createElement";

export const createMatchCanvas = () => {
  const canvas = createElement("canvas");
  canvas.width = MatchConstants.BOARD_WIDTH;
  canvas.height = MatchConstants.BOARD_HEIGHT;
  canvas.tabIndex = 0;
  return canvas;
};
