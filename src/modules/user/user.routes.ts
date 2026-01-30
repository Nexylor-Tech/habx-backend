// user routes 
// declare all the /me endpoint here for the entry point
import { Elysia } from 'elysia';
import { checkSubscriptionExpiry } from './user.service';


export const userRoutes = (app: Elysia) => app
  .get('/me', async ({ u, set }: any) => {
    if (!u) { set.status = 401; return "Unauthorized"; }
    const dbUser = await checkSubscriptionExpiry(u);
    if (!dbUser) { set.status = 404; return "User record missing"; }
    return {
      id: dbUser._id,
      email: dbUser.email,
      name: dbUser.name,
      isPremium: dbUser.is_premium,
      subscriptionTier: dbUser.subscription_tier,
      subscriptionStatus: dbUser.subscription_status,
      subscriptionExpiry: dbUser.subscription_expiry,
      aiUsage: dbUser.ai_generation_count,
      aiLimit: dbUser.ai_generation_limit,
      workspaceLimit: dbUser.workspace_limit,
      createdAt: dbUser.createdAt
    }
  })
