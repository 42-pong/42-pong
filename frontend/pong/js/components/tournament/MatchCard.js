import { Component } from "../../core/Component";
import { MatchEnums } from "../../enums/MatchEnums";
import { createDefaultCard } from "../../utils/elements/div/createDefaultCard";
import { createEndFlexBox } from "../../utils/elements/div/createFlexBox";
import { createThreeColumnLayout } from "../../utils/elements/div/createThreeColumnLayout";
import { createStatusBadge } from "../../utils/tournament/createStatusBadge";
import { PlayerProfile } from "./PlayerProfile";

export class MatchCard extends Component {
  _render() {
    const {
      item: { players, status },
    } = this._getState();

    const player1 =
      players.find((player) => player.team === MatchEnums.Team.ONE) ??
      null;
    const player2 =
      players.find((player) => player.team === MatchEnums.Team.TWO) ??
      null;
    const { result1, result2 } = getMatchResult(player1, player2);

    const statusBadge = createStatusBadge(status);

    const text = createThreeColumnLayout(
      new PlayerProfile({ player: player1, matchResult: result1 }),
      new PlayerProfile({ player: player2, matchResult: result2 }),
      createEndFlexBox(statusBadge),
      5,
      5,
      2,
    );
    const card = createDefaultCard({ text });
    this.append(card);
  }
}

const getMatchResult = (player1, player2) => {
  if (!(player1 && player2))
    return {
      result1: MatchEnums.Result.PENDING,
      result2: MatchEnums.Result.PENDING,
    };

  const { isWin: isWin1 } = player1;
  const { isWin: isWin2 } = player2;

  if (isWin1 === isWin2)
    return {
      result1: MatchEnums.Result.PENDING,
      result2: MatchEnums.Result.PENDING,
    };

  if (isWin1)
    return {
      result1: MatchEnums.Result.WIN,
      result2: MatchEnums.Result.LOSE,
    };
  return {
    result1: MatchEnums.Result.WIN,
    result2: MatchEnums.Result.LOSE,
  };
};
