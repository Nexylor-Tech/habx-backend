import mongoose, { Schema } from 'mongoose';

const LogSchema = new Schema({
  habit_id: { type: Schema.Types.ObjectId, ref: 'Habit', required: true },
  workspace_id: { type: Schema.Types.ObjectId, ref: 'Workspace', required: true },
  date: { type: String, required: true },
  status: { type: Number, required: true }
})

export const Log = mongoose.model('log', LogSchema)


