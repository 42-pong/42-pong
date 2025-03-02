import { Endpoints } from "../../constants/Endpoints";
import { fetchAuthenticatedAllData } from "../utils/fetchAuthenticatedAllData";
import { convertBlockedUserData } from "./convertBlockedUserData";

export async function getBlocks() {
  const { data, error } = await fetchAuthenticatedAllData(
    Endpoints.BLOCKS.default.href,
  );

  const users = error ? [] : data.map(convertBlockedUserData);
  return { users, error };
}
