"use client";

import React, { useState } from "react";
import ThreeJSMap from "./components/Three";
import Leaflet2DMap from "./components/Leaflet2DMap";

const tileUrls = {
  moon: "https://isro-s3.s3.ap-south-1.amazonaws.com/isro-s3/simple-moon/",
  mg: "https://isro-s3.s3.ap-south-1.amazonaws.com/isro-s3/Mg_Si_Intensity/",
  al: "https://isro-s3.s3.ap-south-1.amazonaws.com/isro-s3/Al_Si_Intensity/",
};

const Page = () => {
  const [currentMap, setCurrentMap] = useState("threejs"); // "threejs" or "leaflet"
  const [selectedTile, setSelectedTile] = useState("moon"); // "moon", "mg", "al"
  const [latLon, setLatLon] = useState({
    hovered: null, // Stores the current hovered latitude and longitude
  });

  const switchMap = () => {
    setCurrentMap((prevMap) => (prevMap === "threejs" ? "leaflet" : "threejs"));
  };

  const handleTileChange = (event) => {
    setSelectedTile(event.target.value);
  };

  return (
    <div
      style={{
        position: "relative",
        width: "100%",
        height: "100%",
      }}
    >
      {currentMap === "threejs" ? (
        <ThreeJSMap tileUrl={tileUrls[selectedTile]} setLatLon={setLatLon} />
      ) : (
        <Leaflet2DMap tileUrl={tileUrls[selectedTile]} />
      )}

      {/* Controls */}
      <div
        style={{
          position: "absolute",
          bottom: 20,
          left: "50%",
          transform: "translateX(-50%)",
          display: "flex",
          flexDirection: "row",
          flexWrap: "wrap",
          alignItems: "center",
          gap: "10px",
          padding: "10px 20px",
          background: "rgba(0, 0, 0, 0.8)",
          borderRadius: "10px",
          boxShadow: "0 0 10px rgba(255, 255, 255, 0.5)",
          overflow: "hidden",
          maxWidth: "90%",
          justifyContent: "center",
        }}
      >
        <select
          value={selectedTile}
          onChange={handleTileChange}
          style={{
            padding: "5px 10px",
            borderRadius: "5px",
            cursor: "pointer",
            fontSize: "1rem",
            maxWidth: "100%",
          }}
        >
          <option value="moon">Moon</option>
          <option value="mg">Mg</option>
          <option value="al">Al</option>
        </select>
        <button
          onClick={switchMap}
          style={{
            padding: "10px 20px",
            border: "none",
            borderRadius: "5px",
            background: "dodgerblue",
            color: "white",
            cursor: "pointer",
            fontSize: "1rem",
            maxWidth: "100%",
          }}
        >
          {currentMap === "threejs"
            ? "Switch to Subpixel Map"
            : "Switch to 3D Map"}
        </button>
      </div>

      <div
        style={{
          position: "absolute",
          bottom: 20,
          left: 20,
          padding: "7px",
          backgroundColor: "black",
          borderRadius: "5px",
          boxShadow: "0 0 10px rgba(0, 0, 0, 0.5)",
        }}
      >
        {(selectedTile === "mg" || selectedTile === "al") && (
          <img
            src="scale.png"
            alt="Colour Scale"
            style={{
              height: "300px",
              width: "auto",
            }}
          />
        )}
      </div>
    </div>
  );
};

export default Page;
