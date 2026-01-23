// src/App.ts
// Define the Elysia app here

import { userRoutes } from './modules/user/user.routes';
import { workspaceRoutes } from './modules/workspace/workspace.routes';
import { habitRoutes } from './modules/habit/habit.routes';
import { taskRoutes } from './modules/task/task.routes';
import { swagger } from '@elysiajs/swagger';
import { serverTiming } from '@elysiajs/server-timing';
import { Elysia } from 'elysia'
import { cors } from '@elysiajs/cors'
import { authMiddleware } from './shared/middleware/auth';
import { getAuth } from './shared/services/auth';
import { analyticsRoutes } from './modules/analytics/analytics.routes';

export function createApp() {
  const app = new Elysia();
  const auth = getAuth();

  app.use(cors({ origin: ["http://localhost:5173"], credentials: true }))
    .all("/api/auth/*", ({ request }) => auth.handler(request.clone()))
    .derive(authMiddleware);

  userRoutes(app);
  workspaceRoutes(app);
  habitRoutes(app);
  taskRoutes(app);
  analyticsRoutes(app);
  app.get('/', () => ({ status: 'Elysia fired up' }))

  return app;
}


