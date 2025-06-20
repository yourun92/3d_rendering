import * as THREE from 'three';
import { SVGLoader } from 'three/examples/jsm/loaders/SVGLoader.js';

// Создаем сцену, камеру и рендерер
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth/window.innerHeight, 0.1, 1000);
camera.position.z = 100;

const renderer = new THREE.WebGLRenderer({antialias: true});
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Загрузка SVG
const loader = new SVGLoader();
loader.load('svg_file.svg', function(data) {
  const paths = data.paths;

  // Создаем группу для всех 3D объектов из SVG
  const group = new THREE.Group();

  paths.forEach((path) => {
    const shapes = path.toShapes(true);

    shapes.forEach((shape) => {
      // Экструзия: вытягиваем плоскую форму в 3D
      const geometry = new THREE.ExtrudeGeometry(shape, {
        depth: 10, // высота экструзии
        bevelEnabled: false
      });

      // Материал для 3D модели
      const material = new THREE.MeshBasicMaterial({
        color: path.color,
        side: THREE.DoubleSide
      });

      const mesh = new THREE.Mesh(geometry, material);
      group.add(mesh);
    });
  });

  scene.add(group);
});

// Анимация рендеринга
function animate() {
  requestAnimationFrame(animate);
  renderer.render(scene, camera);
}
animate();