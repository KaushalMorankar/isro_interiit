"use client";
import React, { Suspense, useRef } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, shaderMaterial } from "@react-three/drei";
import { extend } from "@react-three/fiber";
import * as THREE from "three";
import { TIFFLoader } from "three/examples/jsm/loaders/TIFFLoader";

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
    // Increase brightness
    gl_FragColor = vec4(textureColor.rgb * 1.5, 1.0); // Brightness factor 1.5
  }
  `
);

extend({ MoonShaderMaterial });

const Moon = () => {
  const ref = useRef();

  const texture = useRef();
  React.useEffect(() => {
    const loader = new TIFFLoader();
    loader.load("/textures/plot-moon-hmap.tiff", (tiff) => {
      texture.current = tiff;
      ref.current.material.uniforms.textureMap.value = tiff;
    });
  }, []);

  return (
    <mesh ref={ref}>
      <sphereGeometry args={[1, 128, 128]} />
      <moonShaderMaterial />
    </mesh>
  );
};

const Page = () => {
  return (
    <Canvas
      camera={{ position: [0, 0, 5], fov: 50 }}
      style={{ height: "100vh", background: "black" }}
    >
      <ambientLight intensity={0.5} />
      <pointLight position={[10, 10, 10]} />
      <Suspense fallback={null}>
        <Moon />
      </Suspense>
      <OrbitControls panSpeed={0.2} />
    </Canvas>
  );
};

export default Page;
