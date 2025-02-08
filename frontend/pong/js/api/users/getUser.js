import { Endpoints } from "../../constants/Endpoints";
import { fetchData } from "../utils/fetchData";
import { convertUserData } from "./convertUserData";

export async function getUser(userId) {
  const { data, error } = await fetchData(
    Endpoints.USERS.withId(userId).href,
  );

  const user = error ? null : convertUserData(data);
  return { user, error };
}
