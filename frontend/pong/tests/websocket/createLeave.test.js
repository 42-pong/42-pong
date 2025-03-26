import { describe, expect, it } from "vitest";
import { TournamentEnums } from "../../js/enums/TournamentEnums";
import { createLeave } from "../../js/websocket/payload/tournament/createLeave";

describe("(positive cases) Category: TOURNAMENT, type: LEAVE", () => {
  it("simple case", () => {
    const payload = createLeave({
      joinType: TournamentEnums.JoinType.LEAVE,
      tournamentId: 42,
    });
    expect(payload).toStrictEqual({
      type: "LEAVE",
      data: {
        tournament_id: 42,
      },
    });
  });
});
