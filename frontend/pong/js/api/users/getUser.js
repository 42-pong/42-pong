import { Endpoints } from "../../constants/Endpoints";
import { isValidId } from "../../utils/isValidId";
import { fetchAuthenticatedData } from "../utils/fetchAuthenticatedData";
import { convertUserData } from "./convertUserData";

export async function getUser(userId) {
  if (!isValidId(userId)) {
    return {
      user: null,
      error: new Error("userId: not a positive integer"),
    };
  }

  const { data, error } = await fetchAuthenticatedData(
    Endpoints.USERS.withId(userId).href,
  );

  const user = error ? null : convertUserData(data);
  return { user, error };
}
