import { Endpoints } from "../../constants/Endpoints";
import { createPostMethodOption } from "./createPostMethodOption";
import { fetchData } from "./fetchData";

export async function postTotp({ email, password, totp }) {
  const { data, error } = await fetchData(
    Endpoints.TOTP.href,
    createPostMethodOption({ email, password, totp }),
  );

  const tokens = error ? null : data;
  return { tokens, error };
}
