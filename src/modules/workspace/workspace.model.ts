// Workspace Model Schema

import mongoose, { Schema } from 'mongoose';

const WorkspaceSchema = new Schema({
  user_id: { type: String, ref: 'User' },
  name: String,
  goal: String,
  created_at: { type: Date, default: Date.now },
  streak: { type: Number, default: 0 },
  last_completed_date: String
})

export const Workspace = mongoose.model('Workspace', WorkspaceSchema)


