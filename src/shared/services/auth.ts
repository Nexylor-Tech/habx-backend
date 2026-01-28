//shared auth.ts
//Declare betteraut here connect it on middleware

import { betterAuth } from "better-auth";
import { mongodbAdapter } from "better-auth/adapters/mongodb";
import { env } from "../../config";
import { WORKSPACE_LIMITS, AI_LIMITS } from "../../config";
import { Workspace } from "../../modules/workspace/workspace.model";
import { emailService } from "../../modules/email/email.service";

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
      sendResetPassword: async ({ user, url, token }, request) => {
        //TODO: Password Reset
        try {
          await emailService.sendPasswordResetEmail(user.email, token, user.name);
        } catch (error) {
          console.error(`Failed to send password reset email`);
        }
      },
      onPasswordReset: async ({ user }, request) => {
        console.log(`Password has been reset ${user.email} has been reset.`)
      }
    },
    advanced: {
      defaultCookieAttributes: {
        httpOnly: true,
        secure: true,
        sameSite: "none",
        partitioned: true,
      },
    },
    emailVerification: {
      sendVerificationEmail: async ({ user, url, token }) => {
        // const verificationUrl = `${env.BETTER_AUTH_BASE_URL}/api/auth/verify-email?token=${token}&callbackURL=${encodeURIComponent(env.BETTER_AUTH_DOMAIN_URL + '/')}`;
        try {
          await emailService.sendVerificationEmail(user.email, url, token, user.name)
        } catch (error) {
          console.error(`Failed to send verification email`, error);
        }
      }
    },
    socialProviders: {
      google: {
        prompt: "select_account",
        clientId: env.GOOGLE_CLIENT_ID as string,
        clientSecret: env.GOOGLE_CLIENT_SECRET as string,
      },
    },
    user: {
      additionalFields: {
        first_name: { type: "string", required: false },
        last_name: { type: "string", required: false },
        subscription_tier: { type: "string", defaultValue: "free" },
        workspace_limit: { type: "number", defaultValue: WORKSPACE_LIMITS['free'] },
        ai_generation_limit: { type: "number", defaultValue: AI_LIMITS['free'] },
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
