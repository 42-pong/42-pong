export const convertMyInfoData = (userData) => {
  const { id, username, email, display_name, avatar } = userData;

  return {
    id,
    username,
    email,
    displayName: display_name,
    avatar,
  };
};
