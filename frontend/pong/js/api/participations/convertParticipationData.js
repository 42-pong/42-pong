export const convertParticipationData = (participationData) => {
  const {
    id,
    tournament_id,
    user_id,
    participation_name,
    ranking,
    created_at,
    updated_at,
  } = participationData;

  return {
    participationId: id,
    tournamentId: tournament_id,
    userId: user_id,
    displayName: participation_name,
    ranking,
    createdAt: created_at,
    updatedAt: updated_at,
  };
};
