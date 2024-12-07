"use client";

import React, { useRef, useEffect, Suspense, useState } from "react";
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

const Sphere = ({ tileUrl, setLatLon, setLoading }) => {
  const ref = useRef();
  const { raycaster } = useThree();

  useEffect(() => {
    const loader = new THREE.TextureLoader();

    setLoading(true); // Start loading
    loader.load(
      `${tileUrl}0/0/0.jpg`,
      (texture) => {
        if (ref.current) {
          ref.current.material.uniforms.textureMap.value = texture;
          console.log("Texture successfully loaded");
        }
        setLoading(false); // Finish loading
      },
      undefined,
      (error) => {
        console.error("Failed to load texture:", error);
        setLoading(false); // Finish loading even if there was an error
      }
    );
  }, [tileUrl, setLoading]); // Reload texture when tileUrl changes

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
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    return () => {
      console.log("Unmounting ThreeJSMap");
    };
  }, []);

  return (
    <div
      ref={mountRef}
      style={{
        width: "100%",
        height: "100vh",
        background: "black",
        position: "relative",
      }}
    >
      {loading && (
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            width: "100%",
            height: "100%",
            backgroundColor: "rgba(0, 0, 0, 0.9)",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            zIndex: 10,
            color: "white",
            textAlign: "center",
            border: "3px solid white",
            borderRadius: "15px",
            boxShadow: "0 0 20px rgba(255, 255, 255, 0.3)",
          }}
        >
          <img
            src="https://media.giphy.com/media/RgzryV9nRCMHPVVXPV/giphy.gif?cid=790b7611zvyxf3c8z8z8ld9yneh6ma8n1r2msvnywocgsw5v&ep=v1_gifs_search&rid=giphy.gif&ct=g"
            alt="loading"
            style={{
              width: "100px",
              height: "100px",
              marginBottom: "20px",
            }}
          />
          <div
            style={{
              fontSize: "2rem",
              fontWeight: "bold",
              marginBottom: "20px",
            }}
          >
            Loading The Map...
          </div>
          <div
            style={{
              fontSize: "1.2rem",
              marginBottom: "10px",
              animation: "fade-in-out 3s infinite",
            }}
          >
            <span
              style={{
                fontWeight: "bold",
              }}
            >
              -
            </span>{" "}
          </div>
        </div>
      )}
      <Canvas
        camera={{ position: [0, 0, 5], fov: 50 }}
        style={{ height: "100vh", background: "black" }}
      >
        <ambientLight intensity={0.5} />
        <pointLight position={[10, 10, 10]} />
        <Suspense fallback={null}>
          <Sphere
            tileUrl={tileUrl}
            setLatLon={setLatLon}
            setLoading={setLoading}
          />
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
