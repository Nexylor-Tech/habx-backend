//analytics service 
//analytics , suggections, graph

import { AnalyticsCache } from "./analytics.model";
import { User } from "../user/user.model";
import { Habit } from "../habit/habit.model";
import { Log } from "../log/log.model";
import { useGemini } from "../../shared/services/gemini";

export async function generateAiSuggestion(userId: string, goal: string) {
  const dbUser = await User.findById(userId);
  const limit = dbUser?.ai_generation_limit || 10;
  const usage = dbUser?.ai_generation_count || 0;

  if (usage >= limit) throw new Error("Limit reached");
  const prompt = `
    You are an expert habit coach, behavioral psychologist, and wellness guide.

    A user’s primary goal is:
    "${goal}"

    Your task is to generate exactly 20 DAILY habits that strongly and directly support this goal.

    STRICT REQUIREMENTS (DO NOT IGNORE):
    1. Every habit must be:
       - Small and realistic (5–30 minutes OR a clearly measurable quantity)
       - Actionable and concrete (NO vague wording)
       - Easy to complete daily

    2. Each habit MUST include:
       - A specific number, duration, or count
         (e.g. "drink 3 liters of water", "walk 7,000 steps", "meditate for 8 minutes")
       - A clear action that can be tracked as done/not done

    3. The habits must be distributed across these categories:
       - Physical / Practical (fitness, health, productivity)
       - Mental focus / discipline
       - Spiritual or inner growth that is closely related to the goal
         (e.g. mindfulness, gratitude, intention-setting, self-awareness)
       Spiritual habits should feel supportive, grounded, and practical — NOT abstract or religious.

    4. Every habit must clearly relate back to the user's goal.
       If a habit does not support the goal, do NOT include it.

    5. Avoid generic phrases such as:
       - "drink more water"
       - "exercise regularly"
       - "be mindful"
       - "stay positive"
       Replace them with precise actions.

    OUTPUT FORMAT:
    Return ONLY a valid JSON array.
    No markdown.
    No explanations.

    Each object must have exactly these fields:
    - "title": short habit name (2–6 words)
    - "category": one of ["Health", "Fitness", "Wellness", "Learning", "Productivity", "Spiritual"]
    - "icon": one of ["water", "walk", "body", "brain", "mind", "sleep", "food", "listen", "write", "activity"]

    EXAMPLE QUALITY (do NOT reuse):
    - "Drink 3 liters of water"
    - "Stretch hips for 10 minutes"
    - "Write one intention sentence"
    - "Walk 7,000 steps outdoors"
    - "Meditate with breath for 6 minutes"
`
  const result = await useGemini(prompt);
  console.log(result);
  const text = (result || "").trim().replace(/```json|```/g, '');
  console.log(text);
  await User.findByIdAndUpdate(userId, { $inc: { ai_generation_count: 1 } });
  return JSON.parse(text);

}


export async function getAiAnalytics(userId: string, workspaceId: string) {
  const dbUser = await User.findById(userId);
  if (!dbUser || (dbUser.ai_generation_count || 0) >= (dbUser.ai_generation_limit || 10)) {
    throw new Error("Limit reached");
  }

  const cached = await AnalyticsCache.findOne({ workspace_id: workspaceId, type: 'ai_insight' });
  if (cached && (new Date().getTime() - cached.created_at.getTime()) < 86400000) {
    return cached.data;
  }

  const habits = await Habit.find({ workspace_id: workspaceId }).limit(20);
  if (habits.length === 0) {
    return { insight: "Start adding habits!", tips: ["Add a habit"] };
  }
  const summary = habits.map((h: any) => ({ title: h.title, completed: h.completion_count, skipped: h.skip_count }));
  const prompt = ``
  try {
    const result = await useGemini(prompt);
    const text = (result || "").trim().replace(/```json|```/g, '');
    const data = JSON.parse(text);

    await AnalyticsCache.updateOne(
      { workspace_id: workspaceId, type: 'ai_insight' },
      { data, created_at: new Date() },
      { upsert: true }
    );
    await User.findByIdAndUpdate(userId, { $inc: { ai_generation_count: 1 } });
    return data;
  } catch (e) {
    return { insight: "Analysis unavailable", tips: ["Keep going!"] };
  }
}

export async function getWeeklyStats(workspaceId: string) {
  const habits = await Habit.find({ workspace_id: workspaceId });
  const habitIds = habits.map((h: any) => h._id);
  const dates = [];
  for (let i = 6; i >= 0; i--) {
    const d = new Date();
    d.setDate(d.getDate() - i);
    dates.push(d.toISOString().split('T')[0]);
  }

  const results = await Log.aggregate([
    { $match: { habit_id: { $in: habitIds }, date: { $in: dates } } },
    {
      $group: {
        _id: "$date",
        completed: { $sum: { $cond: [{ $eq: ["$status", 1] }, 1, 0] } },
        skipped: { $sum: { $cond: [{ $eq: ["$status", 0] }, 1, 0] } },
      }
    }
  ]);

  const dataMap: any = {};
  results.forEach((r: any) => { dataMap[r._id] = r; });

  return dates.map(d => ({
    date: d,
    completed: dataMap[d]?.completed || 0,
    skipped: dataMap[d]?.skipped || 0
  }));
} 
