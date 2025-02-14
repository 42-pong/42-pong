export const convertFriendData = (friendData) => {
  const {
    friend_user_id,
    friend: { username, display_name, avatar },
  } = friendData;

  return {
    id: friend_user_id.toString(),
    username,
    displayName: display_name,
    avatar,
  };
};
