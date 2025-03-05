import { BootstrapBadge } from "../../bootstrap/components/badge";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Component } from "../../core/Component";
import { MatchEnums } from "../../enums/MatchEnums";
import { TournamentEnums } from "../../enums/TournamentEnums";
import { createCenterFlexBox } from "../../utils/elements/div/createFlexBox";
import { createTextElement } from "../../utils/elements/span/createTextElement";
import { getMatchResult } from "../../utils/match/getMatchResult";
import { createScore } from "../match/createScore";
import { ErrorContainer } from "../utils/ErrorContainer";

export class DashboardStats extends Component {
  constructor(state = {}) {
    super({ userId: null, tournaments: [], matches: [], ...state });
  }

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapFlex.setJustifyContentAround(this);
    BootstrapSizing.setWidth100(this);
    BootstrapSizing.setHeight100(this);
  }

  _render() {
    const { userId, tournaments, matches } = this._getState();
    if (!userId) {
      this._append(new ErrorContainer());
      return;
    }

    const wonMatches = matches.filter((match) =>
      isWin(match, userId),
    );
    const winRate = createTextElement(
      `マッチ勝率: ${(getRate(wonMatches.length, matches.length) * 100).toFixed(2)} %`,
      4,
      BootstrapBadge.setPrimary,
    );
    BootstrapSpacing.setMargin(winRate, 2);

    const wonTournaments = getWonTournaments(tournaments, userId);
    const wonTournamentsIndex = createTextElement(
      `トーナメント優勝: ${wonTournaments.length} / ${tournaments.length}`,
      4,
      BootstrapBadge.setSecondary,
    );
    BootstrapSpacing.setMargin(wonTournamentsIndex, 2);

    const recentResults = createRecentResults(matches, userId);

    this.append(winRate, wonTournamentsIndex, recentResults);
  }
}

const getScore = (match, userId) => {
  const [player1, player2] = match.players;
  switch (userId) {
    case player1.userId:
      return player1.score;
    case player2.userId:
      return player2.score;
    default:
      return 0;
  }
};

const getResult = (match, userId) => {
  const [player1, player2] = match.players;
  const [result1, result2] = getMatchResult(player1, player2);
  switch (userId) {
    case player1.userId:
      return result1;
    case player2.userId:
      return result2;
    default:
      return MatchEnums.Result.PENDING;
  }
};

const isWin = (match, userId) =>
  getResult(match, userId) === MatchEnums.Result.WIN;

const isFinalMatch = (match) =>
  match.status === TournamentEnums.Status.FINISHED &&
  match.roundNumber === 2;

const getWonTournaments = (matches, userId) =>
  matches.filter(
    (match) => isFinalMatch(match) && isWin(match, userId),
  );

const createRecentResults = (matches, userId) => {
  const recentMatches = matches
    .filter(
      (match) => match.status === TournamentEnums.Status.FINISHED,
    )
    .slice()
    .sort((a, b) => b.createdAt - a.createdAt)
    .slice(0, 10);
  const recentResults = recentMatches.map((match) =>
    createScore(getScore(match, userId), getResult(match, userId)),
  );
  const results = createCenterFlexBox(...recentResults);
  return results;
};

const getRate = (num, total) => (total === 0 ? 0 : num / total);
