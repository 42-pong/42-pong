import { Endpoints } from "../../constants/Endpoints";
import { isValidId } from "../../utils/isValidId";
import { deleteStatus } from "../../utils/user/deleteStatus";
import { deleteAuthenticated } from "../utils/deleteAuthenticated";

export async function deleteFriends(userId) {
  if (!isValidId(userId)) {
    return {
      error: new Error("userId: not a valid Id"),
    };
  }
  const { error } = await deleteAuthenticated(
    Endpoints.FRIENDS.withId(userId).href,
  );
  if (!error) deleteStatus(userId);
  return { error };
}
