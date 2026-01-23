// user service 
// declare user services here

import { User } from "./user.model"
import { AI_LIMITS, WORKSPACE_LIMITS } from "../../config";

export const checkSubscriptionExpiry = async (u: any) => {
  if (!u) return null;
  const dbUser = await User.findById(u.id);

  if (!dbUser) return null;
  if (dbUser.subscription_expiry) {
    const expiryDate = new Date(dbUser.subscription_expiry);
    if (new Date() > expiryDate && dbUser.subscription_tier !== 'free') {
      dbUser.subscription_tier = 'free';
      dbUser.is_premium = false;
      dbUser.subscription_status = 'expired';
      dbUser.ai_generation_limit = AI_LIMITS['free'];
      dbUser.workspace_limit = WORKSPACE_LIMITS['free'];
      await dbUser.save();
    }
  }
  return dbUser;
}
