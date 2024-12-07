"use client";

import React, { useRef, useEffect, Suspense } from "react";
import { Canvas, useThree } from "@react-three/fiber";
import { OrbitControls, shaderMaterial } from "@react-three/drei";
import { extend } from "@react-three/fiber";
import * as THREE from "three";

// Define the Shader Material
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
        gl_FragColor = vec4(textureColor.rgb, 1.0);
        }
        `
);

extend({ MoonShaderMaterial });

const Sphere = ({ tileUrl, setLatLon }) => {
  const ref = useRef();
  const { raycaster } = useThree();

  useEffect(() => {
    const loader = new THREE.TextureLoader();

    loader.load(
      `${tileUrl}0/0/0.jpg`,
      (texture) => {
        if (ref.current) {
          ref.current.material.uniforms.textureMap.value = texture;
          console.log("Texture successfully loaded");
        }
      },
      undefined,
      (error) => {
        console.error("Failed to load texture:", error);
      }
    );
  }, [tileUrl]); // Reload texture when tileUrl changes

  // Pointer events remain unchanged
  const onPointerMove = (event) => {
    const intersects = raycaster.intersectObject(ref.current);
    if (intersects.length > 0) {
      const point = intersects[0].point;

      const spherical = new THREE.Spherical();
      spherical.setFromVector3(point);

      const latitude = THREE.MathUtils.radToDeg(Math.PI / 2 - spherical.phi);
      const longitude = THREE.MathUtils.radToDeg(spherical.theta);

      setLatLon((prev) => ({
        ...prev,
        hovered: { latitude, longitude },
      }));
    }
  };

  return (
    <mesh
      ref={ref}
      onPointerMove={onPointerMove}
      onPointerOut={() =>
        setLatLon((prev) => ({
          ...prev,
          hovered: null,
        }))
      }
    >
      <sphereGeometry args={[1, 128, 128]} />
      <moonShaderMaterial />
    </mesh>
  );
};

const ThreeJSMap = ({ tileUrl, setLatLon }) => {
  const mountRef = useRef();

  useEffect(() => {
    return () => {
      console.log("Unmounting ThreeJSMap");
    };
  }, []);

  return (
    <div
      ref={mountRef}
      style={{ width: "100%", height: "100vh", background: "black" }}
    >
      <Canvas
        camera={{ position: [0, 0, 5], fov: 50 }}
        style={{ height: "100vh", background: "black" }}
      >
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        <Suspense fallback={null}>
          <Sphere tileUrl={tileUrl} setLatLon={setLatLon} />
        </Suspense>
        <OrbitControls
          zoomSpeed={0.3}
          panSpeed={0.2}
          minDistance={1.2}
          maxDistance={5}
        />
      </Canvas>
    </div>
  );
};

export default ThreeJSMap;