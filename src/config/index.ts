// src/confic/Index.ts 
// Declare all env variables here
export const env = {
  MONGO_URI: process.env.MONGO_URI,
  GEMINI_API_KEY: process.env.GEMINI_API_KEY,
  BETTER_AUTH_SECRET: process.env.BETTER_AUTH_SECRET,
  BETTER_AUTH_BASE_URL: process.env.BETTER_AUTH_BASE_URL,
  BETTER_AUTH_DOMAIN_URL: process.env.BETTER_AUTH_DOMAIN_URL,
  DODO_API_KEY: process.env.DODO_API_KEY,
  DODO_WEBHOOK_SECRET: process.env.DODO_WEBHOOK_SECRET,
  DODO_ENVIRONMENT: process.env.DODO_ENVIRONMENT,
  PRODUCT_ID_PREMIUM: process.env.PRODUCT_ID_PREMIUM,
  PRODUCT_ID_ELITE: process.env.PRODUCT_ID_ELITE,
}


export const AI_LIMITS: Record<string, number> = { free: 10, premium: 30, elite: 100 }
export const WORKSPACE_LIMITS: Record<string, number> = { free: 1, premium: 20, elite: 100 }

