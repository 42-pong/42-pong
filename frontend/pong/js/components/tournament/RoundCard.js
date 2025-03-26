import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { Component } from "../../core/Component";
import { createElement } from "../../utils/elements/createElement";
import { createDefaultCard } from "../../utils/elements/div/createDefaultCard";
import { createStartFlexBox } from "../../utils/elements/div/createFlexBox";
import { createInlineListItem } from "../../utils/elements/li/createListItem";
import { getTextContent } from "../../utils/i18n/lang";
import { createStatusBadge } from "../../utils/tournament/createStatusBadge";
import { MatchCard } from "../match/MatchCard";
import { ListContainer } from "../utils/ListContainer";

export class RoundCard extends Component {
  _setStyle() {
    BootstrapSizing.setWidth100(this);
  }

  _render() {
    const {
      item: { roundNumber, status, matches },
    } = this._getState();

    const roundName = createElement("span", {
      textContent: `${getTextContent("round")} ${roundNumber}`,
    });
    const statusBadge = createStatusBadge(status);
    BootstrapSpacing.setMarginLeft(statusBadge, 3);

    const title = createStartFlexBox(roundName, statusBadge);

    const matchList = matches
      ? new ListContainer({
          ListItem: MatchCard,
          items: matches,
          createListItem: createInlineListItem,
        })
      : "...";

    const card = createDefaultCard({ title, others: [matchList] });
    this.append(card);
  }
}
