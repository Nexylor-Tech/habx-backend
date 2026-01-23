// habit model
// declare the model schema layouts here
import mongoogse, { Schema } from 'mongoose';
const HabitSchema = new Schema({
  workspace_id: { type: Schema.Types.ObjectId, ref: 'Workspace', required: true },
  title: { type: String, required: true },
  category: { type: String, default: 'General' },
  icon: { type: String, default: 'activity' },
  completion_count: { type: Number, default: 0 },
  skip_count: { type: Number, default: 0 }
})

export const Habit = mongoogse.model('Habit', HabitSchema);
