import { Endpoints } from "../../constants/Endpoints";
import { createPatchMethodOptionForAvatar } from "../utils/createPatchMethodOptionForAvatar";
import { fetchAuthenticatedData } from "../utils/fetchAuthenticatedData";
import { convertUserData } from "./convertUserData";

export async function patchAvatar(avatar) {
  const { data, error } = await fetchAuthenticatedData(
    Endpoints.USERS.me().href,
    createPatchMethodOptionForAvatar({ avatar }),
  );

  const user = error ? null : convertUserData(data);
  return { user, error };
}
