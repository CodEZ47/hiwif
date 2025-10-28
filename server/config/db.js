import dotenv from "dotenv";
import pg from "pg";

dotenv.config({ quiet: true });

const { Pool, Client } = pg;
const connectionString = process.env.DB_URL;

const pool = new Pool({
  connectionString,
});

pool
  .connect()
  .then((client) => {
    console.log("Connected to PostgreSQL");
    client.release();
  })
  .catch((err) => console.error("Database connection error:", err.stack));

export default pool;
