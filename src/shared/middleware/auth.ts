// Auth.ts
// User verification
import { getAuth } from "../services/auth";


export const authMiddleware = async ({ request }: any) => {
  const auth = getAuth();
  // const headers = Object.fromEntries(request.headers.entries());
  const session = await auth.api.getSession({ headers: request.headers });
  return { u: session?.user || null, session: session?.session || null };
};



