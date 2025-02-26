import { Endpoints } from "../../constants/Endpoints";
import { UserSessionManager } from "../../session/UserSessionManager";
import { createDeleteMethodOption } from "./createDeleteMethodOption";
import { createPostMethodOption } from "./createPostMethodOption";
import { fetchData } from "./fetchData";

export const deleteAuthenticated = async (url, isRetry = false) => {
  const accessToken =
    UserSessionManager.getInstance().getAccessToken();

  const options = createDeleteMethodOption();
  try {
    const headers = new Headers(options.headers ?? {});
    headers.append("Authorization", `Bearer ${accessToken}`);

    const res = await fetch(url, { ...options, headers });

    if (res.status === 401 && !isRetry)
      return retryWithRefreshToken(url);
    if (res.status !== 204)
      throw new Error("DELETE: STATUS: NOT 204");
  } catch (error) {
    return { error };
  }
  return { error: null };
};

const retryWithRefreshToken = async (url = {}) => {
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
    return { error };
  }
  return deleteAuthenticated(url, true);
};
