import { Endpoints } from "../../constants/Endpoints";
import { fetchAuthenticatedAllData } from "../utils/fetchAuthenticatedAllData";
import { convertUserData } from "./convertUserData";

export async function getUsers() {
  const { data, error } = await fetchAuthenticatedAllData(
    Endpoints.USERS.default.href,
  );

  const users = error ? [] : data.map(convertUserData);
  return { users, error };
}
