import { getTournaments } from "../../api/tournaments/getTournaments";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { AuthView } from "../../core/AuthView";
import { UserSessionManager } from "../../session/UserSessionManager";
import { extractMatches } from "../../utils/match/extractMatches";
import { DashboardContainer } from "../dashboard/DashboardContainer";
import { ErrorView } from "./ErrorView";
import { LoadingView } from "./LoadingView";

export class DashboardView extends AuthView {
  constructor(state = {}) {
    super({
      isLoading: true,
      isError: false,
      userId: null,
      tournaments: [],
      matches: [],
      ...state,
    });
  }

  _setStyle() {
    BootstrapSizing.setWidth100(this);
    BootstrapSizing.setHeight100(this);
  }

  _onConnect() {
    const userId = UserSessionManager.getInstance().myInfo.observe(
      ({ id }) => id,
    );
    getTournaments(userId).then(({ tournaments, error }) => {
      if (error) {
        this._updateState({
          isLoading: false,
          isError: true,
        });
        return;
      }
      this._updateState({
        isLoading: false,
        tournaments,
        matches: extractMatches(tournaments, userId),
        userId,
      });
    });
  }

  _render() {
    const { isLoading, isError, userId, tournaments, matches } =
      this._getState();
    if (isLoading) {
      this.append(new LoadingView());
      return;
    }
    if (isError) {
      this.append(new ErrorView());
      return;
    }

    const dashboardContainer = new DashboardContainer({
      userId,
      tournaments,
      matches,
    });
    this.append(dashboardContainer);
  }
}
