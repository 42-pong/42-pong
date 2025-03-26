import { Endpoints } from "../../constants/Endpoints";
import { requestStatus } from "../../utils/user/requestStatus";
import { fetchAuthenticatedAllData } from "../utils/fetchAuthenticatedAllData";
import { convertFriendData } from "./convertFriendData";

export async function getFriends() {
  const { data, error } = await fetchAuthenticatedAllData(
    Endpoints.FRIENDS.default.href,
  );

  const users = error ? [] : data.map(convertFriendData);
  users.map((user) => requestStatus(user.id));
  return { users, error };
}
