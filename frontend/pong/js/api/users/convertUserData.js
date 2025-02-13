export const convertUserData = (userData) => {
  return {
    id: userData.id,
    username: userData.username,
    displayName: userData.display_name,
    avatar: userData.avatar,
  };
};
