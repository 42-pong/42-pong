import * as THREE from "three";
import { MatchConstants } from "../../constants/MatchConstants";
import { Component } from "../../core/Component";
import { MatchEnums } from "../../enums/MatchEnums";
import { ThreeUtils } from "../../utils/match/ThreeUtils";

export class MatchRenderer3D extends Component {
  #core;
  #resizeHandler;

  constructor(state = {}) {
    super(state);

    this.#core = ThreeUtils.initThreeJs();
  }

  _onConnect() {
    this.#core.renderer.clear();

    this.#resizeHandler = () => {
      const width = this.clientWidth;
      const height = this.clientHeight;
      const { camera, renderer } = this.#core;

      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height);
    };
    window.addEventListener("resize", this.#resizeHandler);
  }

  _onDisconnect() {
    window.removeEventListener("resize", this.#resizeHandler);
    this.#core.renderer.setAnimationLoop(null);
    this.#core.scene.clear();
  }

  _render() {
    this.#resizeHandler();

    const { scene, camera, renderer } = this.#core;
    this.append(renderer.domElement);

    //
    const width = MatchConstants.BOARD_WIDTH;
    const height = MatchConstants.BOARD_HEIGHT;
    const center = { x: width / 2, y: height / 2 };
    const { entities } = this._getState();

    const paddle1 = ThreeUtils.createPaddleMesh(entities.paddle1);
    const paddle2 = ThreeUtils.createPaddleMesh(entities.paddle2);
    const ball = ThreeUtils.createBallMesh(entities.ball);

    scene.add(
      paddle1,
      paddle2,
      ball,
      ThreeUtils.createBoard(width, height, center),
      ThreeUtils.createDefaultLight(center.x, center.y),
    );

    //
    const { team } = entities;
    const createCameraInitPos = (team) => {
      switch (team) {
        case MatchEnums.Team.ONE:
          return new THREE.Vector3(
            -height / 3,
            center.y,
            -height / 2,
          );
        case MatchEnums.Team.TWO:
          return new THREE.Vector3(
            width + height / 3,
            center.y,
            -height / 2,
          );
        default:
          break;
      }
      return new THREE.Vector3(center.x, height, -height);
    };
    const cameraInitPos = createCameraInitPos(team);
    const adjust_paddle_x = (x) =>
      x + MatchConstants.PADDLE_WIDTH / 2;
    const adjust_paddle_y = (y) =>
      y + MatchConstants.PADDLE_HEIGHT / 2;
    const adjust_ball_x = (x) => x + MatchConstants.BALL_SIZE / 2;
    const adjust_ball_y = (y) => y + MatchConstants.BALL_SIZE / 2;

    const animate = () => {
      paddle1.position.x = adjust_paddle_x(
        entities.paddle1.upperLeft.x,
      );
      paddle1.position.y = adjust_paddle_y(
        entities.paddle1.upperLeft.y,
      );
      paddle2.position.x = adjust_paddle_x(
        entities.paddle2.upperLeft.x,
      );
      paddle2.position.y = adjust_paddle_y(
        entities.paddle2.upperLeft.y,
      );
      ball.position.x = adjust_ball_x(entities.ball.upperLeft.x);
      ball.position.y = adjust_ball_y(entities.ball.upperLeft.y);

      if (
        camera.position.distanceTo(cameraInitPos) > ThreeUtils.EPSILON
      ) {
        camera.up.set(0, 0, -1);
        camera.lookAt(center.x, center.y, 0);
        camera.position.lerp(cameraInitPos, 0.03);
      }

      renderer.render(scene, camera);
    };
    renderer.setAnimationLoop(animate);
  }
}
