import { BootstrapGrid } from "../../bootstrap/layout/grid";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Component } from "../../core/Component";
import { UserSessionManager } from "../../session/UserSessionManager";
import { createAroundFlexBox } from "../../utils/elements/div/createFlexBox";
import { createInlineListItem } from "../../utils/elements/li/createListItem";
import { setHeight } from "../../utils/elements/style/setHeight";
import { MatchCard } from "../match/MatchCard";
import { UserProfile } from "../user/UserProfile";
import { ErrorContainer } from "../utils/ErrorContainer";
import { ListContainer } from "../utils/ListContainer";
import { DashboardStats } from "./DashboardStats";

export class DashboardContainer extends Component {
  constructor(state = {}) {
    super({ userId: null, tournaments: [], matches: [], ...state });
  }

  _setStyle() {
    BootstrapDisplay.setFlex(this);
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

    const myInfo = UserSessionManager.getInstance().myInfo.observe(
      (data) => data,
    );
    const profile = new UserProfile({ user: myInfo });
    BootstrapSpacing.setMargin(profile, 3);

    const stats = new DashboardStats({
      userId,
      matches,
      tournaments,
    });
    BootstrapSpacing.setMargin(stats, 3);

    const dashboardCard = createAroundFlexBox(profile, stats);
    BootstrapFlex.setFlexColumn(dashboardCard);
    BootstrapSizing.setHeight75(dashboardCard);

    const matchHistory = new ListContainer({
      ListItem: MatchCard,
      items: matches,
      createListItem: createInlineListItem,
    });

    setHeight(matchHistory, "75vh");
    BootstrapGrid.setCol(dashboardCard, 4);
    BootstrapGrid.setCol(matchHistory, 6);

    this.append(dashboardCard, matchHistory);
  }
}
