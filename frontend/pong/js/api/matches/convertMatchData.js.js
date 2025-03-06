import { convertStatus } from "../tournaments/convertStatus";

export const convertMatchData = (match) => {
  const {
    id,
    round_id,
    status,
    created_at,
    updated_at,
    participations,
  } = match;

  return {
    matchId: id,
    roundId: round_id,
    status: convertStatus(status),
    createdAt: created_at,
    updatedAt: updated_at,
    players: participations.map((participation) =>
      convertParticipationToPlayer(participation),
    ),
  };
};

const convertParticipationToPlayer = (participation) => {
  const { user_id, team, is_win, scores } = participation;

  return {
    userId: user_id,
    team,
    isWin: is_win,
    scores: scores.map(convertScoreData),
    score: scores.length,
  };
};

const convertScoreData = (score) => {
  const { created_at, pos_x, pos_y } = score;

  return { createdAt: created_at, posX: pos_x, posY: pos_y };
};
