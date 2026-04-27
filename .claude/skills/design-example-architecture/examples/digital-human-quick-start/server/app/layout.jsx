import "./globals.css";

export const metadata = {
  title: "数字人快速开始",
  description: "Next.js 数字人拉流示例",
};

export default function RootLayout({
  children,
}) {
  return (
    <html lang="zh">
      <body className="bg-gray-50">
        <main className="max-w-4xl mx-auto py-8 px-5">{children}</main>
      </body>
    </html>
  );
}
