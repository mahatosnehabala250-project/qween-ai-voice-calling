export const metadata = {
  title: 'Queen Voice AI - AI Phone Agents for India',
  description: '24/7 AI phone agents that speak Hindi & English. Book appointments automatically.',
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body className="antialiased">{children}</body>
    </html>
  );
}
