import dotenv from "dotenv";
import app from "./app.js";

dotenv.config({ quiet: true });
const PORT = process.env.PORT || 8080;

app.listen(PORT, () => {
  console.log("Server is running.");
});
