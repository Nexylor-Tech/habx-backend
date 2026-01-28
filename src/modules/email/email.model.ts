import { transporter } from './transporter';
import { env } from '../../config';

export interface SendEmailParams {
  to: string;
  subject: string;
  text: string;
  html: string;
}

export const sendEmail = async ({ to, subject, text, html }: SendEmailParams) => {
  try {
    const info = transporter.sendMail({
      from: `"HabX" <${env.EMAIL_USER}>`,
      to,
      subject,
      text,
      html,
    });
    console.log(`Email send successfullu to ${to}`);
    return info;
  } catch (error) {
    console.error(`Failed to send email`, error);
    throw error;
  }
};
