export const createPatchMethodOptionForAvatar = ({ avatar }) => {
  const formData = new FormData();
  formData.append("avatar", avatar);
  return {
    method: "PATCH",
    body: formData,
  };
};
