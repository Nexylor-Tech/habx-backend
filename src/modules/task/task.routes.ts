// Task Routes
// Directly using Task Model No need for server bcs of small functionalities


import { Elysia, t } from 'elysia';
import { Workspace } from '../workspace/workspace.model';
import * as TaskService from './task.service'


export const taskRoutes = (app: Elysia) => app
  .get('/tasks', async ({ headers, u, set }: any) => {
    if (!u) { set.status = 401; return []; }
    let workspaceId = headers['x-workspace-id'];
    if (!workspaceId) {
      const firstWs = await Workspace.findOne({ user_id: u.id });
      workspaceId = firstWs?._id;
    }
    return await TaskService.getTask(workspaceId);
  })
  .post('/tasks', async ({ headers, body, u, set }: any) => {
    if (!u) { set.status = 401; return; }
    let workspaceId = headers['x-workspace-id'];
    if (!workspaceId) {
      const firstWs = await Workspace.findOne({ user_id: u.id });
      workspaceId = firstWs?._id;
    }
    return await TaskService.createTask(workspaceId, body.title, body.deadline);
  }, {
    body: t.Object({
      title: t.String(),
      deadline: t.Optional(t.String())
    })
  })
  .patch('/tasks/:id', async ({ params: { id }, body }: any) => {
    return await TaskService.updateTask(id, body);
  }, {
    body: t.Object({
      title: t.Optional(t.String()),
      deadline: t.Optional(t.String()),
      status: t.Optional(t.Number()),
      overdue: t.Optional(t.Number())
    })
  })
