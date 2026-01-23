
import { connectDB } from './src/db';
import { User } from './src/modules/user/user.model';
import mongoose from 'mongoose';

const run = async () => {
  console.log("Connecting...");
  await connectDB();
  console.log("Connected.");

  console.log("Searching for users...");
  try {
    const users = await User.find({});
    console.log(`Found ${users.length} users.`);
    users.forEach(u => {
      console.log(`User ID: ${u._id} (Type: ${typeof u._id})`);
      console.log(`Full doc:`, u.toObject());
    });
  } catch (e) {
    console.error("Error finding users:", e);
  }

  await mongoose.disconnect();
};

run();
