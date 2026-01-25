import Elysia from "elysia";
import { Webhook } from "standardwebhooks";
import { User } from '../user/user.model';
import { env, AI_LIMITS, WORKSPACE_LIMITS } from '../../config';

export const dodoWebhookRoutes = (app: Elysia) => app
  .post('/webhook/dodo', async ({ request, headers, set }: any) => {
    const payload = await request.text();
    const webhookId = headers['webhook-id'];
    const webhookSignature = headers['webhook-signature'];
    const webhookTimestamp = headers['webhook-timestamp'];
    try {
      const wh = new Webhook(env.DODO_WEBHOOK_SECRET);
      wh.verify(payload, {
        'webhook-id': webhookId,
        'webhook-signature': webhookSignature,
        'webhook-timestamp': webhookTimestamp
      });
    } catch (e) {
      set.status = 400; return "Invalid Signature";
    }


    const event = JSON.parse(payload);
    const type = event.type;
    const data = event.data || {}
    // WARN: Add security validation if the user exists or not
    const meta = data.metadata || {}

    if (type === 'subscription.active' || type === 'subscription.renewed' || type === 'subscription.plan_changed') {
      const tier = meta.target_tier;

      await User.findByIdAndUpdate(meta.user_id, {
        is_premium: true,
        subscription_tier: tier,
        subscription_status: 'active',
        ai_generation_limit: meta.ai_generation_limit,
        workspace_limit: meta.workspace_limit,
        subscription_expiry: data.next_billing_date,
        dodo_subscription_id: data.subscription_id
      });
    } else if (type === 'subscription.failed' || type === 'subscription.expired') {
      await User.findByIdAndUpdate(meta.user_id, {
        is_premium: false,
        subscription_tier: 'free',
        ai_generation_limit: AI_LIMITS['free'],
        workspce_limits: WORKSPACE_LIMITS['free'],
        subscription_status: 'inactive'
      });
    }
    return { status: "success" }
  })


