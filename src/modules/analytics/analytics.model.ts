// analytics models
// declare the schema here of the ai prompts

import mongoose, { Schema } from 'mongoose';

const AnalyticsCacheSchema = new Schema({
  workspace_id: { type: Schema.Types.ObjectId, ref: 'Workspace' },
  type: String,
  data: Schema.Types.Mixed,
  created_at: { type: Date, default: Date.now }
});

export const AnalyticsCache = mongoose.model('AnalyticsCache', AnalyticsCacheSchema)
