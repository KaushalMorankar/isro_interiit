import Link from 'next/link'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'

export default function AboutPage() {
  return (
    <div className="min-h-screen bg-gray-900 text-gray-100">
      <header className="border-b border-gray-800">
        <div className="container mx-auto px-4 py-4 flex justify-between items-center">
          <Link href="/" className="text-2xl font-bold">ISRO</Link>
          <nav>
            <ul className="flex space-x-4">
              <li><Link href="/" className="hover:text-blue-400 transition-colors">Home</Link></li>
              <li><Link href="/moon-map" className="hover:text-blue-400 transition-colors">Moon Map</Link></li>
              <li><Link href="/docs" className="hover:text-blue-400 transition-colors">Docs</Link></li>
              <li><Link href="/about" className="hover:text-blue-400 transition-colors">About</Link></li>
            </ul>
          </nav>
        </div>
      </header>

      <main className="py-12">
        <div className="container mx-auto px-4">
          <h1 className="text-4xl font-bold mb-8 text-blue-400">About ISRO</h1>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <CardTitle className="text-blue-400">Our Mission</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-300">
                  The Indian Space Research Organisation (ISRO) is the space agency of India. Our mission is to harness space technology for national development while pursuing space science research and planetary exploration.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <CardTitle className="text-blue-400">History</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-300">
                  ISRO was formed in 1969 and has since led India's space program through numerous successful missions, including lunar and Mars exploration, satellite launches, and development of indigenous launch vehicles.
                </p>
              </CardContent>
            </Card>

            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <CardTitle className="text-blue-400">Key Achievements</CardTitle>
              </CardHeader>
              <CardContent>
                <ul className="list-disc list-inside text-gray-300 space-y-2">
                  <li>Chandrayaan missions for lunar exploration</li>
                  <li>Mars Orbiter Mission (Mangalyaan)</li>
                  <li>Development of PSLV and GSLV launch vehicles</li>
                  <li>Indian Regional Navigation Satellite System (IRNSS)</li>
                </ul>
              </CardContent>
            </Card>

            <Card className="bg-gray-800 border-gray-700">
              <CardHeader>
                <CardTitle className="text-blue-400">Future Plans</CardTitle>
              </CardHeader>
              <CardContent>
                <p className="text-gray-300">
                  ISRO continues to push the boundaries of space exploration with upcoming missions including Gaganyaan (India's first crewed space mission), Chandrayaan-3, and Aditya-L1 solar mission.
                </p>
              </CardContent>
            </Card>
          </div>
        </div>
      </main>

      <footer className="bg-gray-800 py-8 mt-8 border-t border-gray-700">
        <div className="container mx-auto px-4 text-center text-gray-400">
          <p>&copy; 2024 Indian Space Research Organisation. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}
