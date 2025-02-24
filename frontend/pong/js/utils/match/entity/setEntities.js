const init = (entities, gameState) => {
  const { paddle1, paddle2, ball } = gameState;

  entities.paddle1.updateUpperLeft(paddle1);
  entities.paddle2.updateUpperLeft(paddle2);
  entities.ball.updateUpperLeft(ball);
};

const play = (entities, gameState) => {
  const { paddle1, paddle2, ball, score1, score2 } = gameState;

  entities.paddle1.updateUpperLeft(paddle1);
  entities.paddle2.updateUpperLeft(paddle2);
  entities.ball.updateUpperLeft(ball);
  entities.score1.updateScore(score1);
  entities.score2.updateScore(score2);
};

export const setEntities = Object.freeze({
  initStage: init,
  playStage: play,
});
