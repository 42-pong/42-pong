export const createPatchMethodOption = (body) => {
  return {
    method: "PATCH",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  };
};
