const setCookie = (name, value, expiration) => {
  const expirationDate = new Date();
  //cookieの有効期間をexpiration日間にする
  expirationDate.setDate(expirationDate.getDate() + expiration);
  //cookieのセキュリティ設定のベストプラティクスをする必要がある
  document.cookie = `${name}=${value}; expires=${expirationDate.toUTCString()}; "httpOnly: true,secure: true,sameSite: 'strict'"`;
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

const deleteCookie = (name) => {
  // クッキーの有効期限を過去に設定して削除
  document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/; "httpOnly: true,secure: true,sameSite: 'strict'"`;
};

export const Cookie = {
  setCookie,
  getCookie,
  deleteCookie
};
