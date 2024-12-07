"use client";

import React, { useState } from "react";
import ThreeJSMap from "./components/Three";
import Leaflet2DMap from "./components/Leaflet2DMap";

const tileUrls = {
  moon: "http://localhost:8000/tiles_output-simple-moon/",
  mg: "http://localhost:8000/tiles_output_Mg_Si_intensity/",
  al: "http://localhost:8000/tiles_output_Al_Si_intensity/",
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
    <div>
      {currentMap === "threejs" ? (
        <ThreeJSMap tileUrl={tileUrls[selectedTile]} setLatLon={setLatLon} />
      ) : (
        <Leaflet2DMap tileUrl={tileUrls[selectedTile]} />
      )}
      <div
        style={{
          position: "absolute",
          bottom: 20,
          left: "50%",
          transform: "translateX(-50%)",
          display: "flex",
          gap: "10px",
          padding: "10px 20px",
          background: "rgba(0, 0, 0, 0.8)",
          borderRadius: "10px",
          boxShadow: "0 0 10px rgba(255, 255, 255, 0.5)",
        }}
      >
        <select
          value={selectedTile}
          onChange={handleTileChange}
          style={{
            padding: "5px 10px",
            borderRadius: "5px",
            cursor: "pointer",
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
          }}
        >
          {currentMap === "threejs"
            ? "Switch to Leaflet Map"
            : "Switch to Three.js Map"}
        </button>
      </div>
    </div>
  );
};

export default Page;