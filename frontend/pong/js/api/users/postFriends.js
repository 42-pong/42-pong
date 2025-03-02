import { Endpoints } from "../../constants/Endpoints";
import { isValidId } from "../../utils/isValidId";
import { createPostMethodOption } from "../utils/createPostMethodOption";
import { fetchAuthenticatedData } from "../utils/fetchAuthenticatedData";
import { convertFriendData } from "./convertFriendData";

export async function postFriends(userId) {
  if (!isValidId(userId)) {
    return {
      user: null,
      error: new Error("userId: not a valid Id"),
    };
  }

  const { data, error } = await fetchAuthenticatedData(
    Endpoints.FRIENDS.default.href,
    createPostMethodOption({ friend_user_id: userId }),
  );

  const user = error ? null : convertFriendData(data);
  return { user, error };
}
