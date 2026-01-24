//shared auth.ts
//Declare betteraut here connect it on middleware

import { betterAuth } from "better-auth";
import { mongodbAdapter } from "better-auth/adapters/mongodb";
import { env } from "../../config";

import { Workspace } from "../../modules/workspace/workspace.model";

let authInstance: ReturnType<typeof betterAuth> | null = null;

export const createAuth = (mongoClient: any) => {
  if (authInstance) return authInstance;

  authInstance = betterAuth({
    secret: env.BETTER_AUTH_SECRET,
    baseURL: env.BETTER_AUTH_BASE_URL,
    trustedOrigins: [
      env.BETTER_AUTH_DOMAIN_URL,
      "http://localhost:3000",
      "http://localhost:5173",
    ],

    database: mongodbAdapter(mongoClient.db(), mongoClient),
    emailAndPassword: {
      enabled: true,
      disableSignUp: false,
      requireEmailVerification: false,
      minPasswordLength: 8,
      maxPasswordLength: 128,
      autoSignIn: true,
    },
    advanced: {
      defaultCookieAttributes: {
        httpOnly: true,
        secure: true,
        sameSite: "none",
        partitioned: true,
      },
    },
    user: {
      additionalFields: {
        first_name: { type: "string", required: false },
        last_name: { type: "string", required: false },
        subscription_tier: { type: "string", defaultValue: "free" },
        workspace_limit: { type: "number", defaultValue: 1 },
        ai_generation_limit: { type: "number", defaultValue: 10 },
        is_premium: { type: "boolean", defaultValue: false },
      },
    },
    databaseHooks: {
      user: {
        create: {
          after: async (user) => {
            try {
              await Workspace.create({
                user_id: user.id,
                name: "My Workspace",
                goal: "My goal",
              });
            } catch (e) {
              console.error("Error in creating hooks", e);
            }
          },
        },
      },
    },
  });
  return authInstance;
};

export const getAuth = () => {
  if (!authInstance) throw new Error("Auth not initialised");
  return authInstance;
};
