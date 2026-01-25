import { Elysia, t } from "elysia";
import * as PaymentService from './payments.service';

export const paymentRoutes = (app: Elysia) => app
  .post('/payments/checkout', async ({ body, u, set }: any) => {
    if (!u) { set.status = 401; return "Unauthorized"; }
    try {
      return await PaymentService.createCheckout(u, body.tier.toLowerCase());
    } catch (e: any) {
      set.status = e.message === 'Invalid tier' ? 400 : 500;
      return e.message;
    }
  }, {
    body: t.Object({ tier: t.String() })
  })
