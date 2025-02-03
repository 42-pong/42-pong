const setCookie = (token, expiration) => {
  const expirationDate = new Date();
  //cookieの有効期間をexpiration日間にする
  expirationDate.setDate(expirationDate.getDate() + expiration);
  document.cookie = `JWT=${token}; expires=${expirationDate.toUTCString()}`;
};

const getCookie = (name) => {
  const cookieName = `${name}=`;
  const cookies = document.cookie.split(";");
  for (let i = 0; i < cookies.length; i++) {
    let cookie = cookies[i];
    while (cookie.charAt(0) === " ") {
      cookie = cookie.substring(1);
    }
    if (cookie.indexOf(cookieName) === 0) {
      return cookie.substring(cookieName.length, cookie.length);
    }
  }
  return "";
};

export const Cookie = {
  setCookie,
  getCookie,
};
