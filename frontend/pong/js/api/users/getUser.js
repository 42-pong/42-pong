import { Endpoints } from "../../constants/Endpoints";
import { fetchData } from "../utils/fetchData";
import { convertUserData } from "./convertUserData";

export async function getUser(userId) {
  if (!isValid(userId)) {
    return {
      user: null,
      error: new Error("userId: not a 'string' type or empty"),
    };
  }

  const { data, error } = await fetchData(
    Endpoints.USERS.withId(userId).href,
  );

  const user = error ? null : convertUserData(data);
  return { user, error };
}

const isValid = (userId) =>
  typeof userId === "string" && userId !== "";
