import { Endpoints } from "../../constants/Endpoints";
import { fetchAuthenticatedData } from "../utils/fetchAuthenticatedData";
import { convertMyInfoData } from "./convertMyInfoData";

export async function getMyInfo() {
  const { data, error } = await fetchAuthenticatedData(
    Endpoints.USERS.me().href,
  );

  const myInfo = error ? null : convertMyInfoData(data);
  return { myInfo, error };
}
