import { Endpoints } from "../../constants/Endpoints";
import { fetchAuthenticatedAllData } from "../utils/fetchAuthenticatedAllData";
import { convertFriendData } from "./convertFriendData";

export async function getFriends() {
  const { data, error } = await fetchAuthenticatedAllData(
    Endpoints.FRIENDS.default.href,
  );

  const users = error ? [] : data.map(convertFriendData);
  return { users, error };
}
