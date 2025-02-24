import { MatchConstants } from "../../../constants/MatchConstants";
import { BorderEntity } from "../BorderEntity";
import { RectangleEntity } from "./RectangleEntity";
import { ScoreEntity } from "./ScoreEntity";

export const createInitialMatchEntities = () => {
  const paddle1 = new RectangleEntity(
    0,
    0,
    MatchConstants.PADDLE_WIDTH,
    MatchConstants.PADDLE_HEIGHT,
  );

  const paddle2 = new RectangleEntity(
    0,
    0,
    MatchConstants.PADDLE_WIDTH,
    MatchConstants.PADDLE_HEIGHT,
  );

  const ball = new RectangleEntity(
    0,
    0,
    MatchConstants.BALL_SIZE,
    MatchConstants.BALL_SIZE,
  );

  const score1 = new ScoreEntity(
    MatchConstants.BOARD_WIDTH / 2 -
      MatchConstants.SCORE_X_FROM_CENTER,
    MatchConstants.SCORE_Y,
  );

  const score2 = new ScoreEntity(
    MatchConstants.BOARD_WIDTH / 2 +
      MatchConstants.SCORE_X_FROM_CENTER,
    MatchConstants.SCORE_Y,
  );

  const border = new BorderEntity(
    0,
    0,
    MatchConstants.BOARD_WIDTH,
    MatchConstants.BOARD_HEIGHT,
  );

  return { paddle1, paddle2, ball, score1, score2, border };
};
