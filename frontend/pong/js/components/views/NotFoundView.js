import { BootstrapBadge } from "../../bootstrap/components/badge";
import { BootstrapDisplay } from "../../bootstrap/utilities/display";
import { BootstrapFlex } from "../../bootstrap/utilities/flex";
import { BootstrapSizing } from "../../bootstrap/utilities/sizing";
import { View } from "../../core/View";
import { createTextElement } from "../../utils/elements/span/createTextElement";

export class NotFoundView extends View {
  _setStyle() {
    BootstrapDisplay.setFlex(this);
    BootstrapFlex.setAlignItemsCenter(this);
    BootstrapFlex.setJustifyContentCenter(this);
    BootstrapSizing.setHeight100(this);
  }

  _render() {
    const message = createTextElement(
      "ページが見つかりませんでした",
      3,
      BootstrapBadge.setSecondary,
    );
    this.append(message);
  }
}
