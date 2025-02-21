import { getParticipations } from "../../api/participations/getParticipations";
import { BootstrapGrid } from "../../bootstrap/layout/grid";
import { BootstrapBorders } from "../../bootstrap/utilities/borders";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { BootstrapSpacing } from "../../bootstrap/utilities/spacing";
import { TournamentConstants } from "../../constants/TournamentConstants";
import { Component } from "../../core/Component";
import { createElement } from "../../utils/elements/createElement";
import { sliceWithDefaults } from "../../utils/sliceWithDefaults";
import { PlayerProfile } from "./PlayerProfile";

export class TournamentPlayers extends Component {
  static #COLS_PER_ROW = 2;

  constructor(state = {}) {
    super({ tournamentId: null, participations: [], ...state });
  }

  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setFlexColumn(this);
    BootstrapFlex.setJustifyContentCenter(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapSizing.setWidth100(this);
    BootstrapBorders.setBorder(this);
    BootstrapBorders.setRounded(this);
  }

  _onConnect() {
    const { tournamentId } = this._getState();
    getParticipations(tournamentId).then(
      ({ participations, error }) => {
        if (error) return;
        this._updateState({ participations });
      },
    );
  }

  _render() {
    const { participations } = this._getState();
    const createComponent = (item) =>
      new PlayerProfile({ participation: item });
    this.append(
      createGridLayout(
        participations,
        TournamentConstants.PLAYER_NUM,
        TournamentPlayers.#COLS_PER_ROW,
        createComponent,
      ),
    );
  }
}

function createGridLayout(
  items,
  minOutputCount,
  columnsPerRow,
  createComponent,
) {
  const rows = [];
  const outputCount = Math.max(items.length, minOutputCount);

  for (let i = 0; i < outputCount; i += columnsPerRow) {
    const row = createElement("div");
    BootstrapGrid.setRow(row);

    const colsInRow = sliceWithDefaults(items, i, columnsPerRow).map(
      (item) => {
        const col = createElement("div");
        BootstrapGrid.setCol(
          col,
          BootstrapGrid.FULL_COLUMN_COUNT / columnsPerRow,
        );
        col.append(createComponent(item));
        return col;
      },
    );

    row.append(...colsInRow);
    BootstrapSpacing.setMargin(row);
    rows.push(row);
  }

  const container = createElement("div");
  BootstrapGrid.setContainer(container);
  container.append(...rows);
  return container;
}
