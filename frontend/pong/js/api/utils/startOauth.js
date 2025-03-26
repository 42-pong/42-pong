import { Endpoints } from "../../constants/Endpoints";

export async function startOauth() {
  const response = await fetch(Endpoints.OAUTH.href, {
    redirect: "manual",
  });
  if (response.type === "opaqueredirect") {
    window.location.href = response.url;
  }
  return response;
}
