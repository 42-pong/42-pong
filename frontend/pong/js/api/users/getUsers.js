import { Endpoints } from "../../constants/Endpoints";
import { fetchData } from "../utils/fetchData";
import { convertUserData } from "./convertUserData";

export async function getUsers() {
  const { data, error } = await fetchData(
    Endpoints.USERS.default.href,
  );

  const users = error ? [] : data.map(convertUserData);
  return { users, error };
}
