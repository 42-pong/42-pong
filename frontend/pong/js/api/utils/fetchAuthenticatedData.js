import { Endpoints } from "../../constants/Endpoints";
import { UserSessionManager } from "../../session/UserSessionManager";
import { createPostMethodOption } from "./createPostMethodOption";
import { fetchData } from "./fetchData";

export const fetchAuthenticatedData = async (
  url,
  options = {},
  isRetry = false,
) => {
  const result = {
    data: null,
    error: null,
  };

  const accessToken =
    UserSessionManager.getInstance().getAccessToken();

  try {
    const headers = new Headers(options.headers ?? {});
    headers.append("Authorization", `Bearer ${accessToken}`);

    const res = await fetch(url, { ...options, headers });

    if (res.status === 401 && !isRetry)
      return retryWithRefreshToken(url, options);

    const { status, data } = await res.json();
    if (status !== "ok") throw new Error("STATUS: NOT OK");
    result.data = data;
  } catch (error) {
    result.error = error;
  }
  return result;
};

const retryWithRefreshToken = async (url, options = {}) => {
  const refreshToken =
    UserSessionManager.getInstance().getRefreshToken();

  try {
    const { data, error } = await fetchData(
      Endpoints.REFRESH_TOKEN.href,
      createPostMethodOption({ refresh: refreshToken }),
    );
    if (error) throw new Error("Refresh: NOT OK");

    const { access } = data;
    UserSessionManager.getInstance().setAccessToken(access);
  } catch (error) {
    return { data: null, error };
  }
  return fetchAuthenticatedData(url, options, true);
};
