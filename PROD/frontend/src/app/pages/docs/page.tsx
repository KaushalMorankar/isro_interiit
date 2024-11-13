// import { useState } from "react";
// import Link from "next/link";
// import { getSortedDocsData, getDocData } from "@/lib/docs";
// import { Button } from "@/components/ui/button";
// import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
// import { ChevronLeft, ChevronRight } from "lucide-react";
// import ReactMarkdown from "react-markdown";
// import { Sidebar } from "@/components/ui/sidebar"; // Import Sidebar from Shadcn

// interface Doc {
//   id: string;
//   title: string;
//   content: string;
// }

// interface DocsPageProps {
//   allDocs: Doc[];
// }

// const ITEMS_PER_PAGE = 5;

// export async function getStaticProps() {
//   const allDocs = getSortedDocsData();
//   return {
//     props: {
//       allDocs,
//     },
//   };
// }

// const DocsPage: React.FC<DocsPageProps> = ({ allDocs }) => {
//   const [currentPage, setCurrentPage] = useState<number>(1);
//   const [selectedDoc, setSelectedDoc] = useState<Doc | null>(null);

//   const indexOfLastItem = currentPage * ITEMS_PER_PAGE;
//   const indexOfFirstItem = indexOfLastItem - ITEMS_PER_PAGE;
//   const currentDocs = allDocs.slice(indexOfFirstItem, indexOfLastItem);

//   const totalPages = Math.ceil(allDocs.length / ITEMS_PER_PAGE);

//   const handleDocClick = async (id: string) => {
//     const docData = await getDocData(id);
//     setSelectedDoc(docData);
//   };

//   return (
//     <div className="min-h-screen bg-gray-900 text-gray-100">
//       <header className="border-b border-gray-800">
//         <div className="container mx-auto px-4 py-4 flex justify-between items-center">
//           <Link href="/" className="text-2xl font-bold">
//             ISRO
//           </Link>
//           <nav>
//             <ul className="flex space-x-4">
//               <li>
//                 <Link
//                   href="/"
//                   className="hover:text-blue-400 transition-colors"
//                 >
//                   Home
//                 </Link>
//               </li>
//               <li>
//                 <Link
//                   href="/moon-map"
//                   className="hover:text-blue-400 transition-colors"
//                 >
//                   Moon Map
//                 </Link>
//               </li>
//               <li>
//                 <Link
//                   href="/docs"
//                   className="hover:text-blue-400 transition-colors"
//                 >
//                   Docs
//                 </Link>
//               </li>
//               <li>
//                 <Link
//                   href="/about"
//                   className="hover:text-blue-400 transition-colors"
//                 >
//                   About
//                 </Link>
//               </li>
//             </ul>
//           </nav>
//         </div>
//       </header>

//       <main className="py-12">
//         <div className="container mx-auto px-4">
//           <h1 className="text-4xl font-bold mb-8 text-blue-400">
//             Documentation
//           </h1>

//           <div className="flex flex-col md:flex-row gap-8">
//             <div className="w-full md:w-1/4">
//               <Card className="bg-gray-800 border-gray-700">
//                 <CardHeader>
//                   <CardTitle className="text-blue-400">Contents</CardTitle>
//                 </CardHeader>
//                 <CardContent>
//                   <Sidebar className="bg-gray-700 p-4 rounded-lg">
//                     {currentDocs.map((doc) => (
//                       <div
//                         key={doc.id}
//                         onClick={() => handleDocClick(doc.id)}
//                         className="cursor-pointer text-blue-400 hover:text-blue-600 mb-2"
//                       >
//                         {doc.title}
//                       </div>
//                     ))}
//                   </Sidebar>
//                 </CardContent>
//               </Card>
//               <div className="mt-4 flex justify-between">
//                 <Button
//                   onClick={() =>
//                     setCurrentPage((prev) => Math.max(prev - 1, 1))
//                   }
//                   disabled={currentPage === 1}
//                   variant="outline"
//                 >
//                   <ChevronLeft className="mr-2 h-4 w-4" /> Previous
//                 </Button>
//                 <Button
//                   onClick={() =>
//                     setCurrentPage((prev) => Math.min(prev + 1, totalPages))
//                   }
//                   disabled={currentPage === totalPages}
//                   variant="outline"
//                 >
//                   Next <ChevronRight className="ml-2 h-4 w-4" />
//                 </Button>
//               </div>
//             </div>

//             <div className="w-full md:w-3/4">
//               <Card className="bg-gray-800 border-gray-700">
//                 <CardHeader>
//                   <CardTitle className="text-blue-400">
//                     {selectedDoc ? selectedDoc.title : "Select a document"}
//                   </CardTitle>
//                 </CardHeader>
//                 <CardContent>
//                   {selectedDoc ? (
//                     <ReactMarkdown className="prose prose-invert max-w-none">
//                       {selectedDoc.content}
//                     </ReactMarkdown>
//                   ) : (
//                     <p className="text-gray-300">
//                       Please select a document from the sidebar to view its
//                       content.
//                     </p>
//                   )}
//                 </CardContent>
//               </Card>
//             </div>
//           </div>
//         </div>
//       </main>

//       <footer className="bg-gray-800 py-8 mt-8 border-t border-gray-700">
//         <div className="container mx-auto px-4 text-center text-gray-400">
//           <p>
//             &copy; 2024 Indian Space Research Organisation. All rights reserved.
//           </p>
//         </div>
//       </footer>
//     </div>
//   );
// };

// export default DocsPage;
