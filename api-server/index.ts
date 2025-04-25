import express, { urlencoded, json } from "express";
import fs from 'fs/promises';
import path from 'path';

const port = process.env.COMMUNITAS_DATA_PORT ?? process.env.PORT ?? 3000;
const app = express();

const dataDir = path.join(process.cwd(), 'data');

app.use(urlencoded({ extended: true }));
app.use(json());

app.get("/", (req, res) => {
  res.status(200).json({ msg: "Server is up and running" });
});

// just hardcode the path for now

app.get("/api/municipality-doctors/1804", async (req, res) => {
  try {
    const filePath = path.join(dataDir, "municipality-doctors", "dataset", "doctors-1804-2025-04.json");
    const raw = await fs.readFile(filePath, "utf-8");
    const data = JSON.parse(raw);
    res.status(200).json(data);
  } catch (err) {
    console.error("Could not parse JSON:", err);
    res.status(500).json({ error: "Invalid JSON format" });
  }
});

app.listen(port, () => {
  console.log(`Server is listening at port ${port}`);
});