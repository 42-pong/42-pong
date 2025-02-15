export const convertUserData = (userData) => {
  const { id, username, display_name, avatar } = userData;

  return {
    id: id.toString(),
    username,
    displayName: display_name,
    avatar,
  };
};
