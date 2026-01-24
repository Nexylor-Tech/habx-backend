// habit services
// declare the services for the habit routes
import { Habit } from './habit.model';
import { Workspace } from '../workspace/workspace.model';
import { Log } from '../log/log.model';

export async function logHabit(habitId: string, userId: string, date: string, statusVal: number) {
  const habit = await Habit.findById(habitId);
  if (!habit) throw new Error("Habit not found.");

  const ws = await Workspace.findById(habit.workspace_id);
  if (ws?.user_id !== userId) throw new Error("Unauthorized");

  const existing = await Log.findOne({ habit_id: habitId, date });

  if (existing) {
    if (existing.status !== statusVal) {
      const inc = statusVal === 1 ? { completion_count: 1, skip_count: -1 } : { completion_count: -1, skip_count: 1 };
      await Habit.findByIdAndUpdate(habitId, { $inc: inc });
      existing.status = statusVal;
      await existing.save();

    }
  } else {
    await Log.create({
      habit_id: habitId,
      workspace_id: ws?._id,
      date,
      status: statusVal
    });
    const field = statusVal === 1 ? "completion_count" : "skip_count";
    await Habit.findByIdAndUpdate(habitId, { $inc: { [field]: 1 } });

    if (statusVal === 1 && ws) {
      const todayStr = new Date().toISOString().split('T')[0];
      const yesterday = new Date();
      yesterday.setDate(yesterday.getDate() - 1);
      const yesterdayStr = yesterday.toISOString().split('T')[0];
      if (ws.last_completed_date !== todayStr) {
        if (ws.last_completed_date === yesterdayStr) {
          ws.streak += 1;
        } else {
          ws.streak = 1;
        }
        ws.last_completed_date = todayStr;
        await ws.save();
      }
    }
  }
  const updatedHabit = await Habit.findById(habitId);
  const updatedWs = await Workspace.findById(ws?._id);
  return {
    message: "Logged",
    completion_count: updatedHabit?.completion_count,
    skip_count: updatedHabit?.skip_count,
    workspace_streak: updatedWs?.streak
  };

};



