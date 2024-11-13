import axios from "axios";
import { NextApiRequest, NextApiResponse } from "next";

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  const { max_val } = req.query;
  try {
    const response = await axios.get(
      `http://localhost:8000/plot?max_val=${max_val}`,
      {
        responseType: "arraybuffer", // Expecting binary data
      }
    );

    // Send back the binary data as an image response
    res.setHeader("Content-Type", "image/png");
    res.send(Buffer.from(response.data, "binary"));
  } catch (error) {
    console.error("Error fetching plot from FastAPI:", error);
    res.status(500).json({ error: "Error fetching plot" });
  }
}
