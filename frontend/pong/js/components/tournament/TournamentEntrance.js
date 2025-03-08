import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Paths } from "../../constants/Paths";
import { PongEvents } from "../../constants/PongEvents";
import { Component } from "../../core/Component";
import { TournamentEnums } from "../../enums/TournamentEnums";
import { WebSocketEnums } from "../../enums/WebSocketEnums";
import { UserSessionManager } from "../../session/UserSessionManager";
import { createElement } from "../../utils/elements/createElement";
import { getTextContent } from "../../utils/i18n/lang";
import { isValidIdStr } from "../../utils/isValidIdStr";
import { isValidDisplayName } from "../../utils/user/isValidDisplayName";
import { LinkButton } from "../utils/LinkButton";
import { ObservableInput } from "../utils/ObservableInput";
import { TournamentJoinButton } from "./TournamentJoinButton";

export class TournamentEntrance extends Component {
  #entranceButtons;
  #toHome;
  #displayNameInput;
  #tournamentJoinHandler;
  #syncDefaultDisplayName;

  constructor(state = {}) {
    super({ isJoinError: false, ...state });

    this.#tournamentJoinHandler = (payload) => {
      const {
        type,
        data: { status, tournament_id: tournamentId },
      } = payload;
      if (type !== WebSocketEnums.Tournament.Type.JOIN) return;
      if (status !== "OK") {
        this._updateState({ isJoinError: true, tournamentId });
        return;
      }
      this.dispatchEvent(
        PongEvents.UPDATE_TOURNAMENT_STAGE.create(
          TournamentEnums.Stage.PROGRESS,
          tournamentId,
        ),
      );
    };
  }

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setJustifyContentAround(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSizing.setWidth75(this);
    BootstrapSizing.setHeight75(this);

    BootstrapDisplay.setGrid(this.#entranceButtons);
    BootstrapSizing.setWidth50(this.#entranceButtons);
    BootstrapSpacing.setGap(this.#entranceButtons);

    BootstrapSizing.setWidth50(this.#toHome);
    this.#toHome.setSecondary();
  }

  _onConnect() {
    const { defaultTournamentIdStr } = this._getState();

    const defaultDisplayName =
      UserSessionManager.getInstance().myInfo.observe((data) => {
        const { displayName } = data;
        return displayName;
      });

    this.#displayNameInput = new ObservableInput(
      {},
      {
        type: "text",
        placeholder: getTextContent("displayName"),
        value: defaultDisplayName,
      },
    );

    const getDisplayName = () =>
      this.#displayNameInput.subject.observe((data) => {
        const { value } = data;
        if (!isValidDisplayName(value)) {
          this.#displayNameInput.setError();
          return { displayName: null, error: new Error() };
        }
        return { displayName: value, error: null };
      });

    this.#entranceButtons = createTournamentEntranceButtons({
      getDisplayName,
      defaultTournamentIdStr: defaultTournamentIdStr
        ? defaultTournamentIdStr
        : "",
    });

    this.#toHome = new LinkButton({
      textContent: getTextContent("goBack"),
      pathname: Paths.HOME,
    });

    UserSessionManager.getInstance().webSocket.attachHandler(
      WebSocketEnums.Category.TOURNAMENT,
      this.#tournamentJoinHandler,
    );

    this.#syncDefaultDisplayName = ({ displayName }) => {
      this.#displayNameInput.setValue(displayName);
    };
    UserSessionManager.getInstance().myInfo.attach(
      this.#syncDefaultDisplayName,
    );
  }

  _onDisconnect() {
    UserSessionManager.getInstance().webSocket.detachHandler(
      WebSocketEnums.Category.TOURNAMENT,
      this.#tournamentJoinHandler,
    );
    UserSessionManager.getInstance().myInfo.detach(
      this.#syncDefaultDisplayName,
    );
  }

  _render() {
    // TODO: タイトル要素を作成する関数でまとめる
    const title = createElement("h1", {
      textContent: `🏓 ${getTextContent("startTournament")}`,
    });
    const { isJoinError } = this._getState();

    // TODO: エラーメッセージ
    this.append(
      title,
      isJoinError
        ? `[${getTextContent("error")}] ${getTextContent("joiningTournament")}`
        : "",
      this.#displayNameInput,
      this.#entranceButtons,
      this.#toHome,
    );
  }
}

const createTournamentEntranceButtons = ({
  getDisplayName,
  defaultTournamentIdStr,
}) => {
  const joinRandom = new TournamentJoinButton({
    joinType: TournamentEnums.JoinType.RANDOM,
    getDisplayName,
    textContent: getTextContent("randomJoin"),
  });
  joinRandom.setPrimary();

  const joinWithCreation = new TournamentJoinButton({
    joinType: TournamentEnums.JoinType.CREATE,
    getDisplayName,
    textContent: getTextContent("createTournament"),
  });
  joinWithCreation.setOutlinePrimary();

  const joinWithInput = createJoinWithInput({
    getDisplayName,
    defaultTournamentIdStr,
  });

  const container = createElement("div");
  container.append(joinRandom, joinWithCreation, joinWithInput);
  return container;
};

const createJoinWithInput = ({
  getDisplayName,
  defaultTournamentIdStr,
}) => {
  const inputTournamentId = new ObservableInput(
    {},
    {
      type: "text",
      placeholder: `${getTextContent("tournament")} ID`,
      value: defaultTournamentIdStr,
    },
  );
  BootstrapSizing.setWidth50(inputTournamentId);
  BootstrapSpacing.setPadding(inputTournamentId);

  const getTournamentId = () =>
    inputTournamentId.subject.observe((data) => {
      const { value } = data;
      if (!isValidIdStr(value)) {
        inputTournamentId.setError();
        return { id: null, error: new Error() };
      }
      return { id: Number.parseInt(value), error: null };
    });

  const joinButton = new TournamentJoinButton({
    joinType: TournamentEnums.JoinType.SELECTED,
    getDisplayName,
    getTournamentId,
    textContent: getTextContent("join"),
  });
  BootstrapSizing.setWidth50(joinButton);
  BootstrapSpacing.setPadding(joinButton);
  joinButton.setOutlinePrimary();

  const container = createElement("div");
  container.append(inputTournamentId, joinButton);
  BootstrapDisplay.setFlex(container);
  BootstrapFlex.setAlignItemsCenter(container);
  BootstrapFlex.setJustifyContentAround(container);
  return container;
};
