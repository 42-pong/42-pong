import { Endpoints } from "../../constants/Endpoints";
import { isValidId } from "../../utils/isValidId";
import { deleteAuthenticated } from "../utils/deleteAuthenticated";

export async function deleteFriends(userId) {
  if (!isValidId(userId)) {
    return {
      error: new Error("userId: not a valid Id"),
    };
  }
  return await deleteAuthenticated(
    Endpoints.FRIENDS.withId(userId).href,
  );
}
