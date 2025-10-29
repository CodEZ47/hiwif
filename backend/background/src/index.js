import cron from "node-cron";
import { cleanUpTokens } from "./jobs/cleanup.js";
import dotenv from "dotenv";

dotenv.config({ quiet: true });

const schedule = process.env.CRON_SCHEDULE || "* * * * *";

console.log(`Token cleaner started – schedule: ${schedule}`);

cron.schedule(
  schedule,
  async () => {
    try {
      await cleanUpTokens();
    } catch (err) {
      console.error("Cleanup job failed:", err);
    }
  },
  { recoverMissedExecutions: true }
);
