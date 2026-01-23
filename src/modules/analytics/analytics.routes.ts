// analytics routes

import { Elysia, t } from 'elysia';
import { Workspace } from '../workspace/workspace.model';
import * as AnalyticsService from './analytics.service'

export const analyticsRoutes = (app: Elysia) => app
  .post('/generate-suggestions', async ({ body, u, set }: any) => {
    if (!u) { set.status = 401; return "Unauthorized"; }
    try {
      return await AnalyticsService.generateAiSuggestion(u.id, body.goal)
    } catch (e: any) {
      if (e.message === "Limit reached") set.status = 403;
      else set.statu = 503;
      return e.message;
    }
  }, {
    body: t.Object({ goal: t.String() })
  })
  .get('/ai/analytics', async ({ headers, u, set }: any) => {
    if (!u) { set.status = 401; return "Unauthorized"; }
    let workspaceId = headers["x-workspace-id"];
    if (!workspaceId) {
      const firstWs = await Workspace.findOne({ user_id: u.id });
      workspaceId = firstWs?._id;
    }

    try {
      return await AnalyticsService.getAiAnalytics(u.id, workspaceId)
    } catch (e: any) {
      if (e.message === "Limit reached") set.status = 403;
      else set.status = 503;
      return e.message;
    }
  })
  .get('/analytics/weekly/', async ({ headers, u, set }: any) => {
    if (!u) return [];
    let workspaceId = headers['x-workspace-id'];
    if (!workspaceId) {
      const firstWs = await Workspace.findOne({ user_id: u.id });
      workspaceId = firstWs?._id;
    }
    return await AnalyticsService.getWeeklyStats(workspaceId);

  })
