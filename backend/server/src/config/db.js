import dotenv from "dotenv";
import {PrismaClient} from '@prisma/client'

dotenv.config({ quiet: true });

const prisma = new PrismaClient();

async function connectDB() {
    try{
        await prisma.$connect();
        console.log("Connected to DB")
    }catch(err){
        console.log("Database connection error:", err);
        process.exit(1);
    }
}

connectDB()

export default prisma;
