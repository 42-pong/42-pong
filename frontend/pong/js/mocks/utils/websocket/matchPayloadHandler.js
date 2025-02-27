import { delay } from "msw";
import { MatchConstants } from "../../../constants/MatchConstants";
import { MatchEnums } from "../../../enums/MatchEnums";
import { incrementWithBounds } from "../../../utils/incrementWithBounds";
import { incrementWithWrap } from "../../../utils/incrementWithWrap";
import { isPreservingDirectionWithBounds } from "../../../utils/isPreservingDirectionWithBounds";
import { sendMatch } from "./sendPayloads";

const MILLISECONDS_PER_FRAME = 20;

export const matchPayloadHandler = async (
  client,
  payload,
  matchState,
) => {
  const { stage, data } = payload;
  switch (stage) {
    case MatchEnums.Stage.INIT: {
      Object.assign(matchState, getInitialMatchState());
      const { match_id } = data;
      if (match_id) {
        sendMatch(client, MatchEnums.Stage.INIT, {
          team: getRandomTeam(),
          display_name1: "alice",
          display_name2: "bob",
          ...getFilteredMatchState(matchState),
        });
      } else
        sendMatch(
          client,
          MatchEnums.Stage.INIT,
          getFilteredMatchState(matchState),
        );
      break;
    }
    case MatchEnums.Stage.READY: {
      sendMatch(client, MatchEnums.Stage.READY, {});
      matchState.intervalId = setInterval(
        playMatchRoutine,
        MILLISECONDS_PER_FRAME,
        client,
        matchState,
      );

      await delay(10000);
      clearInterval(matchState.intervalId);
      matchState.intervalId = -1;

      const win = getRandomTeam();
      const score1 = win === MatchEnums.Team.ONE ? 5 : 3;
      const score2 = win === MatchEnums.Team.TWO ? 5 : 3;
      sendMatch(client, MatchEnums.Stage.END, {
        win,
        score1,
        score2,
      });
      break;
    }
    case MatchEnums.Stage.PLAY:
      handleUserInput(data, matchState);
      break;
    case MatchEnums.Stage.END:
      clearInterval(matchState.intervalId);
      matchState.intervalId = -1;
      break;
    default:
      break;
  }
};

const getNextBall = (ball, ballDir, ballBounds) => {
  return {
    x: incrementWithBounds(ball.x, ballDir.x, 0, ballBounds.x),
    y: incrementWithBounds(ball.y, ballDir.y, 0, ballBounds.y),
  };
};

const getNextBallDir = (ball, ballDir, ballBounds) => {
  const isDirectionPreservedX = isPreservingDirectionWithBounds(
    ball.x,
    ballDir.x,
    0,
    ballBounds.x,
  );
  const isDirectionPreservedY = isPreservingDirectionWithBounds(
    ball.y,
    ballDir.y,
    0,
    ballBounds.y,
  );
  return {
    x: isDirectionPreservedX ? ballDir.x : -ballDir.x,
    y: isDirectionPreservedY ? ballDir.y : -ballDir.y,
  };
};

const playMatchRoutine = (client, matchState) => {
  const { ball, ballDir, ballBounds } = matchState;
  const nextBall = getNextBall(ball, ballDir, ballBounds);
  const nextBallDir = getNextBallDir(ball, ballDir, ballBounds);

  matchState.ball = nextBall;
  matchState.ballDir = nextBallDir;

  sendMatch(
    client,
    MatchEnums.Stage.PLAY,
    getFilteredMatchState(matchState),
  );
};

const getInitialMatchState = () => {
  return {
    paddle1: { ...MatchConstants.PADDLE_1_INIT_POS },
    paddle2: { ...MatchConstants.PADDLE_2_INIT_POS },
    paddleBound:
      MatchConstants.BOARD_HEIGHT - MatchConstants.PADDLE_HEIGHT,
    ball: { ...MatchConstants.BALL_INIT_POS },
    ballDir: { ...MatchConstants.BALL_INIT_DIR },
    ballBounds: {
      x: MatchConstants.BOARD_WIDTH - MatchConstants.BALL_SIZE,
      y: MatchConstants.BOARD_HEIGHT - MatchConstants.BALL_SIZE,
    },
    score1: MatchConstants.SCORE_1_INIT,
    score2: MatchConstants.SCORE_2_INIT,
    intervalId: -1,
  };
};

const getFilteredMatchState = (matchState) => {
  return {
    paddle1: matchState.paddle1,
    paddle2: matchState.paddle2,
    ball: matchState.ball,
    score1: matchState.score1,
    score2: matchState.score2,
  };
};

const getPaddle = (team, matchState) => {
  switch (team) {
    case MatchEnums.Team.ONE:
      return matchState.paddle1;
    case MatchEnums.Team.TWO:
      return matchState.paddle2;
    default:
      break;
  }
  return null;
};

const getPaddleDelta = (move) => {
  switch (move) {
    case MatchEnums.Move.DOWN:
      return MatchConstants.PADDLE_SPEED;
    case MatchEnums.Move.UP:
      return -MatchConstants.PADDLE_SPEED;
    default:
      return 0;
  }
};

const handleUserInput = (data, matchState) => {
  const { move, team } = data;
  const paddle = getPaddle(team, matchState);
  const paddleDelta = getPaddleDelta(move);
  paddle.y = incrementWithWrap(
    paddle.y,
    paddleDelta,
    0,
    matchState.paddleBound,
  );
};

const getRandomTeam = () => {
  const randomOneOrTwo = Math.floor(Math.random() * 2) + 1;
  return randomOneOrTwo.toString();
};
