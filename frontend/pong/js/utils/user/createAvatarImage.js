import { BootstrapBorders } from "../../bootstrap/utilities/borders";
import { Endpoints } from "../../constants/Endpoints";
import { setHeight } from "../elements/style/setHeight";

export const createAvatarImage = (params) => {
  const { pathname, alt, height } = params;

  const image = new Image();
  image.src = Endpoints.create(pathname).href;
  image.alt = alt;
  image.onerror = () => {
    image.onerror = null;
    image.src = Endpoints.USERS.defaultAvatar.href;
  };
  if (height) setHeight(image, height);
  BootstrapBorders.setRoundedCircle(image);
  return image;
};
