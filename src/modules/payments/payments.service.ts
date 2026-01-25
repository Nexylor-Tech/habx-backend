import { User } from "../user/user.model";
import { env } from "../../config/"
import DodoPayments from "dodopayments";
const client = new DodoPayments({
  bearerToken: env.DODO_API_KEY,
  environment: env.DODO_ENVIRONMENT
});

const PRODUCT_IDS: Record<string, string> = {
  "premium": env.PRODUCT_ID_PREMIUM,
  "elite": env.PRODUCT_ID_ELITE
}
// This createCheckout is where DODO session is implemented 
// and metadata is attached to the request which will be fetched in dodo webhook


export async function createCheckout(u: any, tier: string) {
  const dbUser = await User.findById(u.id);
  const productId = PRODUCT_IDS[tier];
  // get the product data
  const product = client.products.retrieve(productId);
  const productMeta = (await product).metadata
  if (!productId) throw new Error('Invalid tier');

  // If the user has an active subscription => change plan
  if (dbUser?.dodo_subscription_id && dbUser?.subscription_status === 'active') {
    const result = await client.subscriptions.changePlan(dbUser.dodo_subscription_id, {
      product_id: productId,
      proration_billing_mode: 'prorated_immediately',
      quantity: 1
    })
    if (!result) throw new Error("Failed to change plan.");
    console.log("Reached upto here");
    return { status: 'updated', message: `Plan changed to ${tier}` };
  }
  try {
    const session = await client.checkoutSessions.create({
      product_cart: [
        { product_id: productId, quantity: 1 }
      ],
      metadata: {
        user_id: u.id,
        ai_generation_limit: productMeta.ai_generation_limit,
        workspace_limit: productMeta.workspace_limit,
        target_tier: productMeta.subscription_tier
      },
      return_url: `${env.BETTER_AUTH_DOMAIN_URL}/settings?success=true`
    });
    return { checkout_url: session.checkout_url, session_id: session.session_id };
  } catch (e) {
    throw new Error("Payment provider error");
  }
}
