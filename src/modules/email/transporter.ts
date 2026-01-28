import nodemailer from 'nodemailer'
import { env } from '../../config';

export const transporter = nodemailer.createTransport({
  host: 'smtp.hostinger.com',
  port: 465,
  secure: true,
  auth: {
    user: env.EMAIL_USER,
    pass: env.EMAIL_PASSWORD,
  },
});

transporter.verify((error, success) => {
  if (error) {
    console.error('SMTP not running', error);
  } else {
    console.log('SMTP runnning');
  }
});
