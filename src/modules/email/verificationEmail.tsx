import { Html, Body, Container, Head, Heading, Link, Preview, Text } from "@react-email/components";

interface VerificationEmailProps {
  verificationUrl: string;
  userName?: string
}

export default function VerificationEmail(props: VerificationEmailProps) {
  const {
    verificationUrl,
    userName
  } = props;
  return (
    <Html>
      <Head />
      <Preview>Verify your email address</Preview>
      <Body style={main}>
        <Container style={container}>
          <Heading style={h1}>Welcome to our App!</Heading>
          <Text style={text}>
            {userName ? `Hi ${userName}, ` : 'Hi, '}
            Please verify your email address to get started.
          </Text>
          <Link href={verificationUrl} style={button}>
            Verify Email
          </Link>
          <Text style={footer}>
            If you didn't create an account, you can safely ignore this email.
          </Text>
        </Container>
      </Body>
    </Html>
  );
}

const main = {
  backgroundColor: '#f6f9fc',
  fontFamily: '-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Ubuntu,sans-serif',
};

const container = {
  backgroundColor: '#ffffff',
  margin: '0 auto',
  padding: '20px 0 48px',
  marginBottom: '64px',
};

const h1 = {
  color: '#333',
  fontSize: '24px',
  fontWeight: 'bold',
  margin: '40px 0',
  padding: '0',
  textAlign: 'center' as const,
};

const text = {
  color: '#333',
  fontSize: '16px',
  lineHeight: '26px',
  textAlign: 'center' as const,
};

const button = {
  backgroundColor: '#5469d4',
  borderRadius: '4px',
  color: '#fff',
  display: 'block',
  fontSize: '16px',
  fontWeight: 'bold',
  textAlign: 'center' as const,
  textDecoration: 'none',
  padding: '12px 20px',
  margin: '24px auto',
  maxWidth: '200px',
};

const footer = {
  color: '#8898aa',
  fontSize: '14px',
  lineHeight: '24px',
  textAlign: 'center' as const,
  marginTop: '32px',
};

