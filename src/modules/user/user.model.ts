// User.model 
// declare user model schema here

import mongoose, { Schema } from 'mongoose'

const UserSchema = new Schema({
  // NOTE: Betterauth fields
  email: { type: String, required: true, unique: true },
  name: String,
  emailVerified: Boolean,
  image: String,
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now },
  // NOTE: Mongodb fields
  is_premium: { type: Boolean, default: false },
  subscription_tier: { type: String, default: 'free' },
  subscription_status: { type: String, default: 'inactive' },
  subscription_expiry: String,
  ai_generation_count: { type: Number, default: 0 },
  ai_generation_limit: { type: Number, default: 10 },
  workspace_limit: { type: Number, default: 10 },
  dodo_subscription_id: { type: String, default: null }
})

export const User = mongoose.model('User', UserSchema, 'user');
