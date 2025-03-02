import { fetchAuthenticatedData } from "./fetchAuthenticatedData";

export const fetchAuthenticatedAllData = async (
  url,
  options = {},
) => {
  let current = new URL(url);
  current.searchParams.set("page", 1);
  let allData = [];
  while (current) {
    const { data, error } = await fetchAuthenticatedData(
      current.href,
      options,
    );
    if (error) return { data: null, error };

    const { results, next } = data;
    allData = allData.concat(results);
    current = next ? new URL(next) : null;
  }
  return { data: allData, error: null };
};
