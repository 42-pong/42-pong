export const convertUserData = (userData) => {
  const {
    id,
    username,
    display_name,
    avatar,
    is_friend,
    is_blocked,
    match_wins,
    match_losses,
  } = userData;

  return {
    id,
    username,
    displayName: display_name,
    avatar,
    isFriend: is_friend,
    isBlocked: is_blocked,
    matchWins: match_wins,
    matchLosses: match_losses,
  };
};
