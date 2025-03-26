import { BootstrapBadge } from "../../bootstrap/components/badge";
import { BootstrapGrid } from "../../bootstrap/layout/grid";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Component } from "../../core/Component";
import { UserSessionManager } from "../../session/UserSessionManager";
import {
  createAroundFlexBox,
  createCenterFlexBox,
  createDefaultFlexBox,
} from "../../utils/elements/div/createFlexBox";
import { createInlineListItem } from "../../utils/elements/li/createListItem";
import { createTextElement } from "../../utils/elements/span/createTextElement";
import { setHeight } from "../../utils/elements/style/setHeight";
import { getTextContent } from "../../utils/i18n/lang";
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

    const matchHistoryContainer =
      createMatchHistoryContainer(matches);

    BootstrapGrid.setCol(dashboardCard, 4);
    BootstrapGrid.setCol(matchHistoryContainer, 6);

    this.append(dashboardCard, matchHistoryContainer);
  }
}

const createMatchHistoryContainer = (matches) => {
  const title = createTextElement(
    getTextContent("matchHistory"),
    5,
    BootstrapBadge.setPrimary,
  );
  BootstrapSpacing.setMargin(title, 3);

  const matchHistoryPanel =
    matches.length > 0 ? createMatchList(matches) : noMatchHistory();

  const layout = createCenterFlexBox(title, matchHistoryPanel);
  BootstrapFlex.setFlexColumn(layout);
  BootstrapSizing.setHeight100(layout);

  return layout;
};

const noMatchHistory = () => {
  const content = createTextElement(
    getTextContent("noMatchAnnouncement"),
    5,
    BootstrapBadge.setSecondary,
  );

  const wrapper = createDefaultFlexBox(content);
  setHeight(wrapper, "65vh");
  BootstrapSpacing.setMargin(wrapper);

  return wrapper;
};

const createMatchList = (matches) => {
  const matchHistory = new ListContainer({
    ListItem: MatchCard,
    items: matches,
    createListItem: createInlineListItem,
  });
  setHeight(matchHistory, "65vh");
  BootstrapSizing.setWidth100(matchHistory);
  BootstrapSpacing.setMargin(matchHistory);

  return matchHistory;
};
