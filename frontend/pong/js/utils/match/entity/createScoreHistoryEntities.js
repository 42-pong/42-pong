import { MatchConstants } from "../../../constants/MatchConstants";
import { BorderEntity } from "./BorderEntity";
import { ScoreHistoryEntity } from "./ScoreHistoryEntity";

export const createScoreHistoryEntities = (width, ...scores) => {
  const ratio = width / MatchConstants.BOARD_WIDTH;
  const offsetX = 0.05 * width;
  const offsetY = 0.05 * ratio * MatchConstants.BOARD_HEIGHT;
  const scale = 0.9 * ratio;

  const border = new BorderEntity(
    offsetX,
    offsetY,
    MatchConstants.BOARD_WIDTH * scale,
    MatchConstants.BOARD_HEIGHT * scale,
  );
  return [
    border,
    ...scores
      .sort((a, b) => a.createdAt - b.createdAt)
      .map(
        ({ posX, posY }, index) =>
          new ScoreHistoryEntity(
            offsetX + posX * scale,
            offsetY + posY * scale,
            index + 1,
          ),
      ),
  ];
};
