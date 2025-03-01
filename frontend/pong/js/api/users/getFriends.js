import { Endpoints } from "../../constants/Endpoints";
import { fetchAuthenticatedAllData } from "../utils/fetchAuthenticatedAllData";
import { requestStatus } from "../../utils/user/requestStatus";
import { convertFriendData } from "./convertFriendData";

export async function getFriends() {
  const { data, error } = await fetchAuthenticatedAllData(
    Endpoints.FRIENDS.default.href,
  );

  const users = error ? [] : data.map(convertFriendData);
  users.map((user) => requestStatus(user.id));
  return { users, error };
}
