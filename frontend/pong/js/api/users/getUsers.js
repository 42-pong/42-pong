import { Endpoints } from "../../constants/Endpoints";
import { fetchAuthenticatedData } from "../utils/fetchAuthenticatedData";
import { convertUserData } from "./convertUserData";

export async function getUsers() {
  const { data, error } = await fetchAuthenticatedData(
    Endpoints.USERS.default.href,
  );

  const users = error ? [] : data.map(convertUserData);
  return { users, error };
}
