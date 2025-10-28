import express from "express";
import cors from "cors";
import dotenv from "dotenv";
import morgan from "morgan";

dotenv.config({quiet: true});

const app = express();
const PORT = process.env.PORT || 8080;

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
