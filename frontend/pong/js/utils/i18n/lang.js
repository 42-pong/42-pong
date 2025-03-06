// en, jp, fr, language, signin, signout, signup
const dict = {
  en: {
    en: "English",
    jp: "Japanese",
    fr: "French",
    language: "Language",
    signin: "Sign in",
    signout: "Sign out",
    signup: "Sign up",
  },
  jp: {
    en: "英語",
    jp: "日本語",
    fr: "フランス語",
    language: "言語",
    signin: "サインイン",
    signout: "サインアウト",
    signup: "サインアップ",
  },
  fr: {
    en: "Anglais",
    jp: "Japonais",
    fr: "Français",
    language: "Langue",
    signin: "Se connecter",
    signout: "Se déconnecter",
    signup: "S'inscrire",
  },
};

const DEFAULT_LANG = "en";
let lang = DEFAULT_LANG;

export const getLang = () => lang;

export const initLang = () => {
  lang = localStorage.getItem("pong-lang") || DEFAULT_LANG;
};

export const setLang = (langLabel) => {
  if (!Object.keys(dict).includes(langLabel)) return false;
  lang = langLabel;
  localStorage.setItem("pong-lang", lang);
  return true;
};

export const getTextContent = (textKey) =>
  dict[lang][textKey] || textKey;
