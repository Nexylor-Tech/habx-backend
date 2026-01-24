// src/App.ts
// Define the Elysia app here

import { Elysia } from 'elysia'
import { cors } from '@elysiajs/cors'
import { getAuth } from './shared/services/auth';
import { authMiddleware } from './shared/middleware/auth';
import { userRoutes } from './modules/user/user.routes';
import { workspaceRoutes } from './modules/workspace/workspace.routes';
import { habitRoutes } from './modules/habit/habit.routes';
import { taskRoutes } from './modules/task/task.routes';
import { analyticsRoutes } from './modules/analytics/analytics.routes';
import { env } from './config';

export function createApp() {
  const app = new Elysia();
  const auth = getAuth();
  console.log(`Better auth domain: ${env.BETTER_AUTH_DOMAIN_URL}`)
  app.use(cors({
    origin: [env.BETTER_AUTH_DOMAIN_URL],
    credentials: true,
    methods: ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allowedHeaders: ['Content-Type', 'Authorization', 'x-workspace-id']
  }))
    .mount(auth.handler)
    .derive(authMiddleware);


  userRoutes(app);
  workspaceRoutes(app);
  habitRoutes(app);
  taskRoutes(app);
  analyticsRoutes(app);
  app.get('/', () => ({ status: 'Elysia fired up' }))

  return app;
}


