import { useState } from "react";
import axios from "axios";

const PlotPage = () => {
  const [maxVal, setMaxVal] = useState<number>(10); // Number state for the max value
  const [imageUrl, setImageUrl] = useState<string | null>(null); // String | null for the image URL

  // Function to fetch the plot from the FastAPI backend
  const fetchPlot = async () => {
    try {
      const response = await axios.get(
        `http://localhost:8000/plot?max_val=${maxVal}`,
        {
          responseType: "blob", // Expecting a binary response (image)
        }
      );
      // Convert the binary response to a URL and set it to state
      const imageObjectURL = URL.createObjectURL(response.data);
      setImageUrl(imageObjectURL);
    } catch (error) {
      console.error("Error fetching plot:", error);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Plot Viewer</h1>

      {/* Input to set max value */}
      <input
        type="number"
        value={maxVal}
        onChange={(e) => setMaxVal(Number(e.target.value))} // Convert input value to a number
        placeholder="Enter max value"
      />
      <button onClick={fetchPlot}>Fetch Plot</button>

      {/* Display the plot if the image URL is available */}
      {imageUrl && (
        <div>
          <h2>Generated Plot:</h2>
          <img
            src={imageUrl}
            alt="Generated Plot"
            style={{ maxWidth: "100%", height: "auto" }}
          />
        </div>
      )}
    </div>
  );
};

export default PlotPage;
