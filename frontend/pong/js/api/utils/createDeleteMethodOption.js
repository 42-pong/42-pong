export const createDeleteMethodOption = (body = null) => {
  const option = body
    ? {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(body),
      }
    : { method: "DELETE" };
  return option;
};
