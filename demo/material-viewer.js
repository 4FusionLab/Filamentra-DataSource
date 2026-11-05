/**
 * Filamentra single-instance WebGL material specimen.
 * Three.js bundled by CI into dist/assets/material-viewer.js.
 * Approximate appearance, not a calibrated Fusion render.
 */
import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { RoomEnvironment } from "three/addons/environments/RoomEnvironment.js";
import { RoundedBoxGeometry } from "three/addons/geometries/RoundedBoxGeometry.js";

const SPECIMEN_RADIUS_MM = 15;
const SPECIMEN_RADIUS_UNITS = 1.05;
const MM_PER_UNIT = SPECIMEN_RADIUS_MM / SPECIMEN_RADIUS_UNITS;
const WALL_THICKNESS_MM = 2;
const clamp01 = value => Math.max(0, Math.min(1, value));

function mapTexture(texture, tileMM, kind, shape) {
  const width = tileMM?.tile_width_mm || 8;
  const height = tileMM?.tile_height_mm || 8;
  // Reference sphere: 30 mm diameter. A real part would require UV/mesh-specific
  // scaling, so this sample uses a fixed physical specimen convention.
  const repeatX = shape === "sphere" ? (2 * Math.PI * SPECIMEN_RADIUS_MM) / width : 30 / width;
  const repeatY = shape === "sphere" ? (Math.PI * SPECIMEN_RADIUS_MM) / height : 22 / height;
  texture.wrapS = THREE.RepeatWrapping;
  texture.wrapT = THREE.RepeatWrapping;
  texture.repeat.set(repeatX, repeatY);
  texture.colorSpace = THREE.NoColorSpace;
  texture.needsUpdate = true;
}

export async function createMaterialViewer(host, options) {
  const {
    hex, appearance, basePath = "./", shape = "sphere", baseRoughness = appearance.roughness,
  } = options;
  const maps = appearance.textures || {};
  if (!maps.normal_gl || !maps.roughness) throw new Error("Для профиля нет PBR-карт");
  if (!/^#[0-9a-fA-F]{6}$/.test(hex)) throw new Error("Нет числового цвета");

  const renderer = new THREE.WebGLRenderer({
    antialias: true,
    alpha: false,
    powerPreference: "low-power",
  });
  renderer.outputColorSpace = THREE.SRGBColorSpace;
  renderer.toneMapping = THREE.ACESFilmicToneMapping;
  renderer.toneMappingExposure = 1.38;
  renderer.setClearColor(0x1b211d, 1);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.7));
  renderer.domElement.className = "material-canvas";
  renderer.domElement.setAttribute("aria-label", "Интерактивный трёхмерный образец материала");
  renderer.domElement.setAttribute("role", "img");
  host.appendChild(renderer.domElement);

  let destroyed = false;
  let frameId = 0;
  let geometry;
  let normalTexture;
  let roughTexture;
  let material;
  let mesh;
  let environment;
  let pmrem;
  let controls;
  let observer;
  let referenceMap;
  let referenceGeometry;
  let referenceMaterial;
  try {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(32, 1, 0.1, 50);
    camera.position.set(0, 0, 5.6);

    pmrem = new THREE.PMREMGenerator(renderer);
    environment = pmrem.fromScene(new RoomEnvironment(), 0.035);
    scene.environment = environment.texture;
    scene.add(new THREE.HemisphereLight(0xffffff, 0x384239, 1.4));
    const key = new THREE.DirectionalLight(0xffffff, 2.1);
    key.position.set(-3, 5, 7);
    scene.add(key);
    const fill = new THREE.DirectionalLight(0xc2d5e2, 0.72);
    fill.position.set(4, -1, 3);
    scene.add(fill);

    const loader = new THREE.TextureLoader();
    [normalTexture, roughTexture, referenceMap] = await Promise.all([
      loader.loadAsync(basePath + maps.normal_gl),
      loader.loadAsync(basePath + maps.roughness),
      loader.loadAsync(basePath + "assets/brand/4fusionlab-logo.png"),
    ]);
    if (destroyed) {
      normalTexture?.dispose();
      roughTexture?.dispose();
      referenceMap?.dispose();
      return null;
    }

    // The actual 4FusionLab mark, not a synthetic test pattern. Its ivory
    // monogram is occluded by opaque plastics and visible through transparent
    // materials. The plane stays fixed as the specimen rotates in front of it.
    referenceMap.colorSpace = THREE.SRGBColorSpace;
    referenceMaterial = new THREE.MeshBasicMaterial({
      map: referenceMap,
      transparent: true,
      depthWrite: false,
      toneMapped: false,
    });
    referenceGeometry = new THREE.PlaneGeometry(2.65, 2.65);
    const opticalReference = new THREE.Mesh(referenceGeometry, referenceMaterial);
    opticalReference.position.z = -1.35;
    scene.add(opticalReference);

    const transparent = appearance.surface_type === "transparent";
    const transmission = transparent ? clamp01(appearance.transmission ?? 0) : 0;
    // The roughness texture contains the preset's absolute value. A smaller
    // grade-specific roughness can multiply that baseline, not reapply it.
    const roughnessFactor = baseRoughness > 0
      ? clamp01((appearance.roughness ?? baseRoughness) / baseRoughness)
      : 1;
    material = new THREE.MeshPhysicalMaterial({
      // For transmitted dyed light, tint absorption instead of the surface.
      color: new THREE.Color(transmission > 0 ? "#ffffff" : hex),
      metalness: 0, // Silk/metal-colored PLA is still a dielectric.
      // Roughness texture pixels already contain absolute roughness values.
      roughness: roughnessFactor,
      roughnessMap: roughTexture,
      normalMap: normalTexture,
      normalScale: new THREE.Vector2(0.65, 0.65),
      transmission,
      opacity: 1, // alpha is not optical transmission
      thickness: transmission > 0 ? WALL_THICKNESS_MM / MM_PER_UNIT : 0,
      attenuationColor: new THREE.Color(hex),
      attenuationDistance: transmission > 0
        ? (appearance.attenuation_distance_mm ?? 10) / MM_PER_UNIT
        : Infinity,
      ior: appearance.ior || 1.46,
      side: THREE.FrontSide,
    });
    const generateGeometry = current =>
      current === "sphere"
        ? new THREE.SphereGeometry(1.05, 88, 64)
        : new RoundedBoxGeometry(2.1, 1.52, 0.28, 5, 0.1);

    let currentShape = shape;
    geometry = generateGeometry(currentShape);
    mesh = new THREE.Mesh(geometry, material);
    mesh.rotation.y = -0.28;
    mesh.rotation.x = -0.12;
    scene.add(mesh);
    mapTexture(normalTexture, maps, "normal", currentShape);
    mapTexture(roughTexture, maps, "rough", currentShape);

    controls = new OrbitControls(camera, renderer.domElement);
    controls.enablePan = false;
    controls.enableZoom = false;
    controls.enableDamping = true;
    controls.dampingFactor = 0.08;
    controls.autoRotate = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    controls.autoRotateSpeed = 0.85;

    function resize() {
      if (destroyed) return;
      const width = Math.max(1, host.clientWidth);
      const height = Math.max(1, host.clientHeight);
      camera.aspect = width / height;
      camera.updateProjectionMatrix();
      renderer.setSize(width, height, false);
    }
    observer = new ResizeObserver(resize);
    observer.observe(host);
    resize();

    function animate() {
      if (destroyed) return;
      frameId = requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    }
    animate();

    return {
      setShape(next) {
        if (destroyed || !["sphere", "coupon"].includes(next)) return;
        currentShape = next;
        geometry.dispose();
        geometry = generateGeometry(next);
        mesh.geometry = geometry;
        mapTexture(normalTexture, maps, "normal", next);
        mapTexture(roughTexture, maps, "rough", next);
      },
      destroy() {
        if (destroyed) return;
        destroyed = true;
        cancelAnimationFrame(frameId);
        observer?.disconnect();
        controls?.dispose();
        scene.remove(mesh);
        geometry?.dispose();
        material?.dispose();
        normalTexture?.dispose();
        roughTexture?.dispose();
        environment?.dispose();
        pmrem?.dispose();
        referenceMap?.dispose();
        referenceMaterial?.dispose();
        referenceGeometry?.dispose();
        renderer.dispose();
        renderer.forceContextLoss();
        renderer.domElement.remove();
      },
    };
  } catch (error) {
    destroyed = true;
    cancelAnimationFrame(frameId);
    observer?.disconnect();
    controls?.dispose();
    geometry?.dispose();
    material?.dispose();
    normalTexture?.dispose();
    roughTexture?.dispose();
    environment?.dispose();
    pmrem?.dispose();
    referenceMap?.dispose();
    referenceMaterial?.dispose();
    referenceGeometry?.dispose();
    renderer.dispose();
    renderer.forceContextLoss();
    renderer.domElement.remove();
    throw error;
  }
}
