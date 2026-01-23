// habit routes
// declare all routes of habit here 
import { Elysia, t } from 'elysia';
import { Workspace } from '../workspace/workspace.model';
import { Log } from '../log/log.model';
import { Habit } from './habit.model';
import { logHabit } from './habit.service';

export const habitRoutes = (app: Elysia) => app
  .get('/habits', async ({ headers, u, set }: any) => {
    if (!u) { set.status = 401; return []; }

    let workspaceId = headers['x-workspace-id'];
    if (!workspaceId) {
      const firstWs = await Workspace.findOne({ user_id: u.id });
      if (!firstWs) { set.status = 404; return []; }
      workspaceId = firstWs._id.toString();
    }

    const habits = await Habit.find({ workspace_id: workspaceId }).lean();
    const today = new Date().toISOString().split('T')[0];
    const habitIds = habits.map((h: any) => h._id);
    const logs = await Log.find({ habit_id: { $in: habitIds }, date: today });
    const logMap = new Map(logs.map((l: any) => [l.habit_id.toString(), l.status]));

    return habits.map((h: any) => ({
      ...h,
      today_status: logMap.get(h._id.toString())
    }));

  })
  .post('/habits', async ({ headers, body, u, set }: any) => {
    if (!u) { set.status = 401; return "Unauthorized"; }

    let workspaceId = headers['x-workspace-id'];
    if (!workspaceId) {
      const firstWs = await Workspace.findOne({ user_id: u.id });
      workspaceId = firstWs?._id;
    }

    const habit = await Habit.create({
      workspace_id: workspaceId,
      title: body.title,
      category: body.category,
      icon: body.icon
    });
    return habit;
  }, {
    body: t.Object({
      title: t.String(),
      category: t.String(),
      icon: t.Optional(t.String())
    })
  })
  .post('/habits/:id/log', async ({ params: { id }, body, u, set }: any) => {
    if (!u) { set.status = 401; return; }
    const statusVal = body.status;
    if (![0, 1].includes(statusVal)) { set.status = 400; return "Invalid status"; }

    try {
      return await logHabit(id, u.id, body.date, statusVal);
    } catch (e: any) {
      if (e.message === "Unauthorized") set.status = 403;
      else if (e.message === "Habit not found") set.status = 404;
      else set.status = 500;
      return e.message;
    }
  }, {
    body: t.Object({
      date: t.String(),
      status: t.Number()
    })
  })
