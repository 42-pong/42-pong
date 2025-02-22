import { Endpoints } from "../../constants/Endpoints";
import { fetchAuthenticatedData } from "../utils/fetchAuthenticatedData";
import { convertFriendData } from "./convertFriendData";

export async function getFriends() {
  // TODO: 認証つきのものに変更
  const { data, error } = await fetchAuthenticatedData(
    Endpoints.FRIENDS.href,
  );

  const users = error ? [] : data.map(convertFriendData);
  return { users, error };
}
