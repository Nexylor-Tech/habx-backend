// db.ts
// Declare mongo db connection here
// Connect with better auth adapter

import mongoose from "mongoose";
import { env } from './config';




const clientOptions = { serverApi: { version: '1', strict: true, deprecationErrors: true } };
export const connectDB = async () => {
  try {
    await mongoose.connect(env.MONGO_URI, clientOptions);
    console.log("Database Online");
    console.log(env.MONGO_URI)
    return mongoose.connection.getClient();
  } catch (e) {
    console.error("Database failed", e);
    process.exit(1)
  }
}


