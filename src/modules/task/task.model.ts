// Task Model 
// Declare the task schema here


import mongoose, { Schema } from "mongoose";

const TaskSchema = new Schema({
  workspace_id: { type: Schema.Types.ObjectId, ref: 'Workspace' },
  title: String,
  deadline: String,
  status: { type: Number, default: 0 },
  overdue: { type: Number, default: 0 }
})

export const Task = mongoose.model('Task', TaskSchema);
