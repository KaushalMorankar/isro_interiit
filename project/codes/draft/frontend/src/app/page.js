"use client";
import React, { Suspense, useRef, useState } from "react";
import { Canvas, useThree } from "@react-three/fiber";
import { OrbitControls, shaderMaterial } from "@react-three/drei";
import { extend } from "@react-three/fiber";
import * as THREE from "three";

const MoonShaderMaterial = shaderMaterial(
  {
    textureMap: null,
  },
  `
  varying vec2 vUv;

  void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
  }
  `,
  `
  uniform sampler2D textureMap;
  varying vec2 vUv;

  void main() {
    vec4 textureColor = texture2D(textureMap, vUv);
    gl_FragColor = vec4(textureColor.rgb * 1.5, 1.0); // Brightness factor 1.5
  }
  `
);

extend({ MoonShaderMaterial });

const Moon = ({ setLatLon }) => {
  const ref = useRef();
  const [hovered, setHovered] = useState(false);
  const { raycaster } = useThree();

  React.useEffect(() => {
    const loader = new THREE.TextureLoader();
    loader.load("/textures/moon.jpg", (texture) => {
      ref.current.material.uniforms.textureMap.value = texture;
    });
  }, []);

  const onPointerMove = (event) => {
    const intersects = raycaster.intersectObject(ref.current);
    if (intersects.length > 0) {
      setHovered(true);
      const point = intersects[0].point;

      // Convert to spherical coordinates
      const spherical = new THREE.Spherical();
      spherical.setFromVector3(point);

      const latitude = THREE.MathUtils.radToDeg(Math.PI / 2 - spherical.phi);
      const longitude = THREE.MathUtils.radToDeg(spherical.theta);

      setLatLon({ latitude, longitude });
    } else {
      setHovered(false);
    }
  };

  return (
    <mesh
      ref={ref}
      onPointerMove={onPointerMove}
      onPointerOut={() => setHovered(false)}
    >
      <sphereGeometry args={[1, 128, 128]} />
      <moonShaderMaterial />
    </mesh>
  );
};

const Page = () => {
  const [latLon, setLatLon] = useState({ latitude: 0, longitude: 0 });

  return (
    <>
      <Canvas
        camera={{ position: [0, 0, 5], fov: 50 }}
        style={{ height: "100vh", background: "black" }}
      >
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        <Suspense fallback={null}>
          <Moon setLatLon={setLatLon} />
        </Suspense>
        <OrbitControls panSpeed={0.2} />
      </Canvas>
      <div
        style={{
          position: "absolute",
          top: 10,
          left: 10,
          color: "white",
          background: "rgba(0, 0, 0, 0.5)",
          padding: "10px",
          borderRadius: "5px",
        }}
      >
        <div>Latitude: {latLon.latitude.toFixed(2)}</div>
        <div>Longitude: {latLon.longitude.toFixed(2)}</div>
      </div>
    </>
  );
};

export default Page;
