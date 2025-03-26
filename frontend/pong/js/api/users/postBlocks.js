import { Endpoints } from "../../constants/Endpoints";
import { isValidId } from "../../utils/isValidId";
import { createPostMethodOption } from "../utils/createPostMethodOption";
import { fetchAuthenticatedData } from "../utils/fetchAuthenticatedData";
import { convertBlockedUserData } from "./convertBlockedUserData";

export async function postBlocks(userId) {
  if (!isValidId(userId)) {
    return {
      user: null,
      error: new Error("userId: not a valid Id"),
    };
  }

  const { data, error } = await fetchAuthenticatedData(
    Endpoints.BLOCKS.default.href,
    createPostMethodOption({ blocked_user_id: userId }),
  );

  const user = error ? null : convertBlockedUserData(data);
  return { user, error };
}
