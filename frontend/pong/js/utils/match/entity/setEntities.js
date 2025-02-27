import { MatchConstants } from "../../../constants/MatchConstants";

const initStage = (entities, data) => {
  const {
    team,
    display_name1,
    display_name2,
    paddle1,
    paddle2,
    ball,
  } = data;

  entities.team = team ?? null;
  entities.displayName1 = display_name1 ?? "";
  entities.displayName2 = display_name2 ?? "";
  entities.paddle1.updateUpperLeft(paddle1);
  entities.paddle2.updateUpperLeft(paddle2);
  entities.ball.updateUpperLeft(ball);
};

const playStage = (entities, data) => {
  const { paddle1, paddle2, ball, score1, score2 } = data;

  entities.paddle1.updateUpperLeft(paddle1);
  entities.paddle2.updateUpperLeft(paddle2);
  entities.ball.updateUpperLeft(ball);
  entities.score1.updateScore(score1);
  entities.score2.updateScore(score2);
};

const endStage = (entities, data) => {
  const { win, score1, score2 } = data;
  entities.win = win;
  entities.score1.updateScore(score1);
  entities.score2.updateScore(score2);
  entities.ball.updateUpperLeft(MatchConstants.BALL_INIT_POS);
};

export const setEntities = Object.freeze({
  initStage,
  playStage,
  endStage,
});
