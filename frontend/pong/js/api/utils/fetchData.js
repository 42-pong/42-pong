export const fetchData = async (url, options = {}) => {
  const result = {
    data: null,
    error: null,
  };

  try {
    const res = await fetch(url, options);
    const { status, data } = await res.json();
    if (status !== "ok") throw new Error("STATUS: NOT OK");
    result.data = data;
  } catch (error) {
    result.error = error;
  }
  return result;
};
