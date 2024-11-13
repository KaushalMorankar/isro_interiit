import Image from "next/image";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { MoonIcon, RocketIcon, MapIcon } from "lucide-react";

export default function HomePage() {
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
                  href="/maps/moon-map"
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
                  href="/pages/about"
                  className="hover:text-blue-400 transition-colors"
                >
                  About
                </Link>
              </li>
            </ul>
          </nav>
        </div>
      </header>

      <main>
        <section className="py-20 relative overflow-hidden">
          <div className="container mx-auto px-4 relative z-10">
            <div className="max-w-3xl">
              <h1 className="text-5xl font-bold mb-4 text-blue-400">
                Exploring the Lunar Frontier
              </h1>
              <p className="text-xl mb-8 text-gray-300">
                Discover ISRO's groundbreaking lunar missions and scientific
                achievements
              </p>
              <Button asChild>
                <Link href="/moon-map">
                  Explore Moon Map <MapIcon className="ml-2 h-4 w-4" />
                </Link>
              </Button>
            </div>
          </div>
          <Image
            src="https://svs.gsfc.nasa.gov/vis/a000000/a004700/a004720/lroc_color_poles_1k.jpg"
            alt="Lunar Albedo Map"
            width={800}
            height={400}
            className="absolute top-1/2 right-0 transform -translate-y-1/2 translate-x-1/4 opacity-50 rounded-full"
          />
        </section>

        <section className="py-20 bg-gray-800">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold mb-8 text-center text-blue-400">
              Chandrayaan-2 Mission
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <Card className="bg-gray-700 border-gray-600">
                <CardHeader>
                  <CardTitle className="text-blue-400">
                    Mission Overview
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-300">
                    Chandrayaan-2 is India's second lunar exploration mission,
                    consisting of an orbiter, lander, and rover. Launched on
                    July 22, 2019, it aims to explore the Moon's south polar
                    region and expand our understanding of lunar geology.
                  </p>
                </CardContent>
              </Card>
              <Card className="bg-gray-700 border-gray-600">
                <CardHeader>
                  <CardTitle className="text-blue-400">
                    CLASS Instrument
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-300">
                    The Chandrayaan-2 Large Area Soft X-ray Spectrometer (CLASS)
                    is designed to measure the abundance of elements such as
                    Magnesium, Aluminium, Silicon, Calcium, Titanium, and Iron
                    on the lunar surface using X-ray fluorescence spectroscopy
                    technique.
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>

        <section className="py-20">
          <div className="container mx-auto px-4">
            <h2 className="text-3xl font-bold mb-8 text-center text-blue-400">
              Key Findings
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
              <Card className="bg-gray-700 border-gray-600">
                <CardHeader>
                  <RocketIcon className="w-12 h-12 mb-4 text-blue-400" />
                  <CardTitle className="text-blue-400">
                    Elemental Composition
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-300">
                    CLASS has provided detailed maps of major elements present
                    on the lunar surface, enhancing our understanding of the
                    Moon's geological evolution.
                  </p>
                </CardContent>
              </Card>
              <Card className="bg-gray-700 border-gray-600">
                <CardHeader>
                  <MoonIcon className="w-12 h-12 mb-4 text-blue-400" />
                  <CardTitle className="text-blue-400">Polar Regions</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-300">
                    The mission has gathered crucial data about the Moon's polar
                    regions, including the presence of water ice and other
                    volatile substances.
                  </p>
                </CardContent>
              </Card>
              <Card className="bg-gray-700 border-gray-600">
                <CardHeader>
                  <MapIcon className="w-12 h-12 mb-4 text-blue-400" />
                  <CardTitle className="text-blue-400">
                    Surface Mapping
                  </CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-gray-300">
                    High-resolution mapping of the lunar surface has revealed
                    new insights into crater formations, lava tubes, and other
                    geological features.
                  </p>
                </CardContent>
              </Card>
            </div>
          </div>
        </section>
      </main>

      <footer className="bg-gray-800 py-8 border-t border-gray-700">
        <div className="container mx-auto px-4 text-center text-gray-400">
          <p>
            &copy; 2024 Indian Space Research Organisation. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}
