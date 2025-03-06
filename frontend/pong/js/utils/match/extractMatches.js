export const extractMatches = (tournaments, userId) =>
  tournaments
    .map((tournament) =>
      tournament.rounds.map((round) =>
        round.matches.filter((match) => hasRelation(match, userId)),
      ),
    )
    .flat(Number.POSITIVE_INFINITY);

const hasRelation = (match, userId) =>
  match.players.some((player) => player.userId === userId);
