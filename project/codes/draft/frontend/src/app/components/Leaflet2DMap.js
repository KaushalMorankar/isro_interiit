"use client";

import React, { useEffect, useRef } from "react";
import "leaflet/dist/leaflet.css";

const Leaflet2DMap = ({ tileUrl }) => {
  const mapRef = useRef(null); // Store the Leaflet map instance
  const tileLayerRef = useRef(null); // Store the tile layer instance

  useEffect(() => {
    const initializeMap = async () => {
      const L = (await import("leaflet")).default;

      // Initialize the map only once
      if (!mapRef.current) {
        const map = L.map("map", {
          center: [0, 0],
          zoom: 3,
          zoomControl: true,
          crs: L.CRS.EPSG3857,
        });

        // Create the initial tile layer
        const tileLayer = L.tileLayer(`${tileUrl}{z}/{x}/{y}.jpg`, {
          maxZoom: 10,
          minZoom: 2,
          attribution: "Custom Moon Map Tiles",
          noWrap: false,
        }).addTo(map);

        // Store references to the map and tile layer
        mapRef.current = map;
        tileLayerRef.current = tileLayer;

        const bounds = L.latLngBounds([-85, -180], [85, 180]);
        map.setMaxBounds(bounds);

        map.on("drag", () => {
          map.panInsideBounds(bounds, { animate: false });
        });

        console.log("Leaflet map initialized!");
      }
    };

    initializeMap();
  }, []);

  // Update the tile layer when tileUrl changes
  useEffect(() => {
    if (tileLayerRef.current) {
      tileLayerRef.current.setUrl(`${tileUrl}{z}/{x}/{y}.jpg`);
      console.log("Leaflet tile layer updated!");
    }
  }, [tileUrl]); // React when tileUrl changes

  return (
    <div
      id="leaflet-container"
      style={{
        height: "97vh",
        width: "98vw",
        overflow: "hidden",
        position: "relative",
        zIndex: 0,
        margin: "0 auto",
      }}
    >
      <div
        id="map"
        style={{
          height: "100%",
          width: "100%",
          overflow: "hidden",
        }}
      ></div>
    </div>
  );
};

export default Leaflet2DMap;
