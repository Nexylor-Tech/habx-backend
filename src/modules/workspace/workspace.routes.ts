// Workspace.routes.ts
// declare all workspace routes here imported from workspace.service

import { Elysia, t } from 'elysia'
import { Workspace } from './workspace.model'
import { User } from '../user/user.model'
import { Habit } from '../habit/habit.model'
import { Task } from '../task/task.model'
import { Log } from '../log/log.model'
// TODO: ADD Tasks and Analytics here
import { updateWorkspaceStreaks } from './workspace.service';

export const workspaceRoutes = (app: Elysia) => app
  .get('/workspaces', async ({ u, set }: any) => {
    if (!u) { set.status = 401; return []; }
    return await updateWorkspaceStreaks(u.id);
  })
  .post('/workspaces', async ({ body, u, set }: any) => {
    if (!u) { set.status = 401; return "Unauthorized"; }
    try {
      const dbUser = await User.findById(u.id);
      const count = await Workspace.countDocuments({ user_id: u.id });

      if (dbUser && count >= (dbUser.workspace_limit || 1)) {
        set.status = 403; return "Workspace limit reached";
      }

      const newWs = await Workspace.create({
        user_id: u.id,
        name: body.name,
        goal: body.goal || "My goal"
      })

      if (body.initial_habits && body.initial_habits.length > 0) {
        const habits = body.initial_habits.map((h: any) => ({
          workspace_id: newWs._id,
          title: h.title,
          category: h.category || 'General',
          icon: h.icon || "activity"
        }));
        await Habit.insertMany(habits);
      }
      console.log(newWs)
      return newWs.toObject();
    } catch (e) {
      console.error("Workspace creation error", e);
      set.status = 500;
      return "Failed to create workspace";
    }
  }, {
    body: t.Object({
      name: t.String(),
      goal: t.Optional(t.String()),
      initial_habits: t.Optional(t.Array(t.Object({
        title: t.String(),
        category: t.Optional(t.String()),
        icon: t.Optional(t.String())
      })))
    })
  })
  .patch('/workspaces/:id', async ({ params: { id }, body, u, set }: any) => {
    if (!u) { set.status = 401; return 'Unauthorized'; }
    const ws = await Workspace.findOneAndUpdate(
      { _id: id, user_id: u.id },
      { $set: body },
      { new: true }
    );
    if (!ws) { set.status = 404; return "Workspace not found"; }
    return ws.toObject();
  }, {
    body: t.Object({
      name: t.Optional(t.String()),
      goal: t.Optional(t.String())
    })
  })
  .delete('/workspaces/:id', async ({ params: { id }, u, set }: any) => {
    if (!u) { set.status = 401; return "Unauthorized"; }
    const ws = await Workspace.findOne({ _id: id, user_id: u.id });
    if (!ws) { set.status = 404; return "Workspace not found"; }
    await Habit.deleteMany({ workspace_id: id });
    console.log("Habits deleted")
    await Task.deleteMany({ workspace_id: id });
    console.log("Tasks deleted")
    await Log.deleteMany({ workspace_id: id });
    console.log("Logs deleted")
    console.log(id)
    // TODO: Add other fields to be deleted before workspace
    await Workspace.deleteOne({ _id: id });

    return { message: "Workspace Deleted" };
  })

