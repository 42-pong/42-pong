import { Endpoints } from "../../constants/Endpoints";
import { isValidId } from "../../utils/isValidId";
import { fetchData } from "../utils/fetchData";
import { convertUserData } from "./convertUserData";

export async function getUser(userId) {
  if (!isValidId(userId)) {
    return {
      user: null,
      error: new Error("userId: not a positive integer"),
    };
  }

  const { data, error } = await fetchData(
    Endpoints.USERS.withId(userId).href,
  );

  const user = error ? null : convertUserData(data);
  return { user, error };
}
