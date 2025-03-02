import { Endpoints } from "../../constants/Endpoints";
import { fetchAuthenticatedData } from "../utils/fetchAuthenticatedData";
import { convertBlockedUserData } from "./convertBlockedUserData";

export async function getBlocks() {
  const { data, error } = await fetchAuthenticatedData(
    Endpoints.BLOCKS.default.href,
  );

  const users = error ? [] : data.map(convertBlockedUserData);
  return { users, error };
}
