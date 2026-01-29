import VerificationEmail from "./templates/verificationEmail"; //ignore the error related to jsx
import PasswordResetEmail from "./templates/passwordResetEmail"; //ignore the error related to jsx
import { render } from "@react-email/components";
import { sendEmail } from '../../modules/email/email.model'
import { env } from '../../config'


export const emailService = {
  sendVerificationEmail: async (to: string, url: string, token: string, userName?: string) => {
    const verificationUrl = `${env.BETTER_AUTH_DOMAIN_URL}/verify-email?token=${token}`;
    const emailHtml = await render(
      VerificationEmail({
        verificationUrl,
        userName,
      })
    )
    return sendEmail({
      to,
      subject: "Verify your email address",
      text: `Click the link to verify your email: ${verificationUrl}`,
      html: emailHtml,
    });
  },

  sendPasswordResetEmail: async (to: string, token: string, userName?: string) => {
    const resetUrl = `${env.BETTER_AUTH_DOMAIN_URL}/reset-password?token=${token}`;
    const emailHtml = await render(
      PasswordResetEmail({
        resetUrl,
        userName,
      })
    )
    return sendEmail({
      to,
      subject: "Reset your password",
      text: `Click the link to reset your password: ${resetUrl}`,
      html: emailHtml,
    });
  },
};

