import { Component } from "../../core/Component";
import { TournamentEnums } from "../../enums/TournamentEnums";
import { createInlineListItem } from "../../utils/elements/li/createListItem";
import { ListContainer } from "../utils/ListContainer";
import { RoundCard } from "./RoundCard";

const MIN_ROUND_NUMBER = 1;
const MAX_ROUND_NUMBER = 2;

export class TournamentScoreboard extends Component {
  _render() {
    const {
      tournamentState: { rounds, status },
    } = this._getState();
    const sortedRounds = createSortedRounds(rounds);
    const isInitiallyScrolled =
      status === TournamentEnums.Status.FINISHED;

    const roundList = new ListContainer({
      ListItem: RoundCard,
      items: sortedRounds,
      createListItem: createInlineListItem,
      isInitiallyScrolled,
    });
    //
    this.append(roundList);
  }
}

const createSortedRounds = (rounds) => {
  const sortedRounds = [];
  for (
    let roundNumber = MIN_ROUND_NUMBER;
    roundNumber <= MAX_ROUND_NUMBER;
    ++roundNumber
  ) {
    const round =
      rounds.find((round) => round.roundNumber === roundNumber) ??
      createDefaultRound(roundNumber);
    sortedRounds.push(round);
  }
  return sortedRounds;
};

const createDefaultRound = (roundNumber) => {
  return {
    roundNumber,
    status: TournamentEnums.Status.WAITING,
    matches: [],
  };
};
