import { Endpoints } from "../../constants/Endpoints";
import { isValidDisplayName } from "../../utils/user/isValidDisplayName";
import { createPatchMethodOption } from "../utils/createPatchMethodOption";
import { fetchAuthenticatedData } from "../utils/fetchAuthenticatedData";
import { convertUserData } from "./convertUserData";

export async function patchMyInfo({ displayName }) {
  if (!isValidDisplayName(displayName)) {
    return {
      user: null,
      error: new Error("displayName: not a valid display name"),
    };
  }

  const { data, error } = await fetchAuthenticatedData(
    Endpoints.USERS.me().href,
    createPatchMethodOption({ display_name: displayName }),
  );

  const user = error ? null : convertUserData(data);
  return { user, error };
}
