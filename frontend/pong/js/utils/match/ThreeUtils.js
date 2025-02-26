import * as THREE from "three";
import { RoundedBoxGeometry } from "three/examples/jsm/geometries/RoundedBoxGeometry.js";

const PALETTE = {
  WARM_BROWN: 0x964b00,
  COOL_BEIGE: 0xf5f5dc,
  SOFT_CREAM: 0xfff599,
  MUTED_GRAY: 0xc7c5b8,
  EARTHY_TAN: 0xd2b48c,
};
const BOARD_DEPTH = 10;
const EPSILON = 0.001;

const initThreeJs = () => {
  const camera = new THREE.PerspectiveCamera(75, 1, 0.1, 1000);
  camera.position.z = 100;
  return {
    scene: new THREE.Scene(),
    camera,
    renderer: new THREE.WebGLRenderer({ antialias: true }),
  };
};

const createBoard = (width, height, center) => {
  const geometry = new RoundedBoxGeometry(
    width + 4,
    height + 4,
    BOARD_DEPTH,
    5,
  );
  const material = new THREE.MeshPhongMaterial({
    color: PALETTE.MUTED_GRAY,
    shininess: 150,
    specular: 0x444444,
  });

  const board = new THREE.Mesh(geometry, material);
  board.position.x = center.x;
  board.position.y = center.y;
  board.position.z = BOARD_DEPTH / 2;
  return board;
};

const createDefaultLight = (x, y) => {
  const light = new THREE.PointLight(0xffffff, 100000, 1000000);
  light.position.set(x, y, -300);
  return light;
};

const createPaddleMesh = (rectangleEntity) => {
  const { width, height } = rectangleEntity.size;

  const geometry = new RoundedBoxGeometry(width, height, 20, 5, 3);
  const material = new THREE.MeshPhongMaterial({
    color: PALETTE.WARM_BROWN,
    shininess: 150,
    specular: 0x444444,
  });
  return new THREE.Mesh(geometry, material);
};

const createBallMesh = (rectangleEntity) => {
  const { width: radius } = rectangleEntity.size;

  const geometry = new THREE.SphereGeometry(radius);
  const material = new THREE.MeshPhongMaterial({
    color: PALETTE.SOFT_CREAM,
    shininess: 150,
    specular: 0x444444,
  });
  return new THREE.Mesh(geometry, material);
};

export const ThreeUtils = Object.freeze({
  PALETTE,
  EPSILON,
  initThreeJs,
  createBoard,
  createDefaultLight,
  createPaddleMesh,
  createBallMesh,
});
