"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { Slider } from "@/components/ui/slider";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { ZoomInIcon, ZoomOutIcon, HomeIcon } from "lucide-react";

const MOON_RADIUS = 1737.1; // km

interface ElementData {
  [key: string]: number[][];
}

const mockElementData: ElementData = {
  silicon: Array.from({ length: 180 }, () =>
    Array.from({ length: 360 }, () => Math.random())
  ),
  magnesium: Array.from({ length: 180 }, () =>
    Array.from({ length: 360 }, () => Math.random())
  ),
  calcium: Array.from({ length: 180 }, () =>
    Array.from({ length: 360 }, () => Math.random())
  ),
  iron: Array.from({ length: 180 }, () =>
    Array.from({ length: 360 }, () => Math.random())
  ),
};

export default function MoonMap() {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [zoom, setZoom] = useState(1);
  const [center, setCenter] = useState({ x: 0, y: 0 });
  const [isDragging, setIsDragging] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [selectedElement, setSelectedElement] = useState("silicon");
  const [heatmapOpacity, setHeatmapOpacity] = useState(0.5);
  const [moonTexture, setMoonTexture] = useState<HTMLImageElement | null>(null);

  useEffect(() => {
    const img = new window.Image();
    img.src =
      "https://svs.gsfc.nasa.gov/vis/a000000/a004700/a004720/lroc_color_poles_1k.jpg";
    img.onload = () => {
      setMoonTexture(img);
    };
  }, []);

  useEffect(() => {
    if (!moonTexture) return;

    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const drawMoon = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // Draw moon surface with texture
      ctx.save();
      ctx.translate(canvas.width / 2 + center.x, canvas.height / 2 + center.y);
      ctx.scale(zoom, zoom);
      ctx.beginPath();
      ctx.arc(0, 0, MOON_RADIUS, 0, Math.PI * 2);
      ctx.closePath();
      ctx.clip();
      ctx.drawImage(
        moonTexture,
        -MOON_RADIUS,
        -MOON_RADIUS,
        MOON_RADIUS * 2,
        MOON_RADIUS * 2
      );
      ctx.restore();

      // Draw heat map
      ctx.globalAlpha = heatmapOpacity;
      const elementData = mockElementData[selectedElement];
      for (let lat = -90; lat < 90; lat++) {
        for (let lon = -180; lon < 180; lon++) {
          const x =
            canvas.width / 2 +
            MOON_RADIUS *
              Math.cos((lat * Math.PI) / 180) *
              Math.sin((lon * Math.PI) / 180) *
              zoom +
            center.x;
          const y =
            canvas.height / 2 -
            MOON_RADIUS * Math.sin((lat * Math.PI) / 180) * zoom +
            center.y;

          const dataValue = elementData[lat + 90][lon + 180];
          const hue = (1 - dataValue) * 240; // Blue (240) for low values, Red (0) for high values
          ctx.fillStyle = `hsla(${hue}, 100%, 50%, ${heatmapOpacity})`;
          ctx.fillRect(x, y, 2 * zoom, 2 * zoom);
        }
      }
      ctx.globalAlpha = 1;
    };

    drawMoon();
  }, [zoom, center, selectedElement, heatmapOpacity, moonTexture]);

  const handleZoomIn = () => setZoom((prev) => Math.min(prev * 1.2, 10));
  const handleZoomOut = () => setZoom((prev) => Math.max(prev / 1.2, 0.5));

  const handleMouseDown = (e: React.MouseEvent<HTMLCanvasElement>) => {
    setIsDragging(true);
    setDragStart({ x: e.clientX - center.x, y: e.clientY - center.y });
  };

  const handleMouseMove = (e: React.MouseEvent<HTMLCanvasElement>) => {
    if (!isDragging) return;
    setCenter({
      x: e.clientX - dragStart.x,
      y: e.clientY - dragStart.y,
    });
  };

  const handleMouseUp = () => {
    setIsDragging(false);
  };

  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      <header className="border-b border-gray-800">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold">
            ISRO
          </Link>
          <nav>
            <ul className="flex space-x-4">
              <li>
                <Link
                  href="/"
                  className="hover:text-blue-400 transition-colors"
                >
                  Home
                </Link>
              </li>
              <li>
                <Link
                  href="/moon-map"
                  className="hover:text-blue-400 transition-colors"
                >
                  Moon Map
                </Link>
              </li>
              <li>
                <Link
                  href="#"
                  className="hover:text-blue-400 transition-colors"
                >
                  Missions
                </Link>
              </li>
              <li>
                <Link
                  href="#"
                  className="hover:text-blue-400 transition-colors"
                >
                  About
                </Link>
              </li>
            </ul>
          </nav>
        </div>
      </header>

      <main className="py-8">
        <div className="container mx-auto px-4">
          <h1 className="text-3xl font-bold mb-4 text-blue-400">
            Interactive Moon Surface Map
          </h1>
          <p className="mb-8 text-gray-300">
            Explore the elemental composition of the Moon's surface based on
            Chandrayaan-2 data.
          </p>

          <div className="flex flex-col lg:flex-row gap-8">
            <Card className="bg-gray-800 border-gray-700 p-4 flex-grow">
              <canvas
                ref={canvasRef}
                width={800}
                height={600}
                className="w-full h-auto cursor-move rounded-lg"
                onMouseDown={handleMouseDown}
                onMouseMove={handleMouseMove}
                onMouseUp={handleMouseUp}
                onMouseLeave={handleMouseUp}
              />
              <div className="mt-4 flex justify-center space-x-2">
                <Button onClick={handleZoomIn} size="icon" variant="outline">
                  <ZoomInIcon />
                </Button>
                <Button onClick={handleZoomOut} size="icon" variant="outline">
                  <ZoomOutIcon />
                </Button>
                <Button
                  onClick={() => {
                    setZoom(1);
                    setCenter({ x: 0, y: 0 });
                  }}
                  size="icon"
                  variant="outline"
                >
                  <HomeIcon />
                </Button>
              </div>
            </Card>

            <Card className="bg-gray-800 border-gray-700 p-4 lg:w-64">
              <CardHeader>
                <CardTitle className="text-blue-400">Controls</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label
                    htmlFor="element-select"
                    className="block text-sm font-medium mb-1 text-gray-300"
                  >
                    Select Element
                  </label>
                  <Select
                    value={selectedElement}
                    onValueChange={setSelectedElement}
                  >
                    <SelectTrigger id="element-select">
                      <SelectValue placeholder="Select element" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="silicon">Silicon</SelectItem>
                      <SelectItem value="magnesium">Magnesium</SelectItem>
                      <SelectItem value="calcium">Calcium</SelectItem>
                      <SelectItem value="iron">Iron</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div>
                  <label
                    htmlFor="heatmap-opacity"
                    className="block text-sm font-medium mb-1 text-gray-300"
                  >
                    Heatmap Opacity
                  </label>
                  <Slider
                    id="heatmap-opacity"
                    min={0}
                    max={1}
                    step={0.1}
                    value={[heatmapOpacity]}
                    onValueChange={([value]) => setHeatmapOpacity(value)}
                  />
                </div>

                <div className="p-4 bg-gray-700 rounded-lg">
                  <h3 className="font-semibold mb-2 text-blue-400">Legend</h3>
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 bg-blue-500"></div>
                    <span className="text-gray-300">Low concentration</span>
                  </div>
                  <div className="flex items-center space-x-2">
                    <div className="w-4 h-4 bg-red-500"></div>
                    <span className="text-gray-300">High concentration</span>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>

      <footer className="bg-gray-800 py-8 mt-8 border-t border-gray-700">
        <div className="container mx-auto px-4 text-center text-gray-400">
          <p>
            &copy; 2024 Indian Space Research Organisation. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}
