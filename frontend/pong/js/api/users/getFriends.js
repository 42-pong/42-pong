import { Endpoints } from "../../constants/Endpoints";
import { fetchData } from "../utils/fetchData";
import { convertFriendData } from "./convertFriendData";

export async function getFriends() {
  // TODO: 認証つきのものに変更
  const { data, error } = await fetchData(Endpoints.FRIENDS.href);

  const users = error ? [] : data.map(convertFriendData);
  return { users, error };
}
