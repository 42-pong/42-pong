import { convertStatus } from "./convertStatus";

export const convertTournamentData = (tournamentData) => {
  const { id, status, created_at, updated_at, rounds } =
    tournamentData;

  return {
    tournamentId: id,
    status: convertStatus(status),
    createdAt: created_at,
    updatedAt: updated_at,
    rounds: rounds.map((round) => convertRoundData(round, id)),
  };
};

const convertRoundData = (round, tournamentId) => {
  const { round_number, status, created_at, updated_at, matches } =
    round;

  return {
    tournamentId,
    roundNumber: round_number,
    status: convertStatus(status),
    createdAt: created_at,
    updatedAt: updated_at,
    matches: matches.map((match) =>
      convertMatchData(match, tournamentId),
    ),
  };
};

const convertMatchData = (match, tournamentId) => {
  const {
    id,
    round_id,
    status,
    created_at,
    updated_at,
    participations,
  } = match;

  return {
    tournamentId,
    matchId: id,
    roundId: round_id,
    status: convertStatus(status),
    createdAt: created_at,
    updatedAt: updated_at,
    players: participations.map((participation) =>
      convertParticipationToPlayer(participation, tournamentId),
    ),
  };
};

const convertParticipationToPlayer = (
  participation,
  tournamentId,
) => {
  const { user_id, team, is_win, scores } = participation;

  return {
    tournamentId,
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
