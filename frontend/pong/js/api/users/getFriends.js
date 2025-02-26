import { Endpoints } from "../../constants/Endpoints";
import { fetchAuthenticatedData } from "../utils/fetchAuthenticatedData";
import { convertFriendData } from "./convertFriendData";

export async function getFriends() {
  const { data, error } = await fetchAuthenticatedData(
    Endpoints.FRIENDS.default.href,
  );

  const users = error ? [] : data.map(convertFriendData);
  return { users, error };
}
