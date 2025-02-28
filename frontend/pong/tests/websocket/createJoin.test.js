import { describe, expect, it } from "vitest";
import { TournamentEnums } from "../../js/enums/TournamentEnums";
import { createJoin } from "../../js/websocket/payload/tournament/createJoin";

describe("(positive cases) Category: TOURNAMENT, type: JOIN", () => {
  it("JoinType: CREATE", () => {
    const payload = createJoin({
      joinType: TournamentEnums.JoinType.CREATE,
      tournamentId: null,
      displayName: "pong",
    });
    expect(payload).toStrictEqual({
      type: "JOIN",
      data: {
        join_type: "CREATE",
        tournament_id: null,
        participation_name: "pong",
      },
    });
  });

  it("JoinType: RANDOM", () => {
    const payload = createJoin({
      joinType: TournamentEnums.JoinType.RANDOM,
      tournamentId: null,
      displayName: "pong",
    });
    expect(payload).toStrictEqual({
      type: "JOIN",
      data: {
        join_type: "RANDOM",
        tournament_id: null,
        participation_name: "pong",
      },
    });
  });

  it("JoinType:.SELECTED", () => {
    const payload = createJoin({
      joinType: TournamentEnums.JoinType.SELECTED,
      tournamentId: 42,
      displayName: "pong",
    });
    expect(payload).toStrictEqual({
      type: "JOIN",
      data: {
        join_type: "SELECTED",
        tournament_id: 42,
        participation_name: "pong",
      },
    });
  });
});
