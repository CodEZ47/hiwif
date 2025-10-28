import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import morgan from "morgan";
import pool from "./config/db.js";

dotenv.config({quiet: true});

const app = express();
const PORT = process.env.PORT || 8080;

app.get("/", async (req, res) => {
  try {
    const result = await pool.query("SELECT NOW()");
    res.json({ time: result.rows[0].now });
  } catch (err) {
    console.error("Query error:", err);
    res.status(500).json({ error: "Database query failed" });
  }
});

app.use(cors());
app.use(morgan("dev"));
app.use(express.json());

app.get("/", (req, res) => {
  res.send("Server is UP!!");
});

app.get("/health", (req, res) => {
  res.status(200).json({ satus: "ok", uptime: process.uptime() });
});

app.listen(PORT, () => {
  console.log("Server is running.");
});
