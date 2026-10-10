import type { Metadata, Viewport } from "next";
import { GeistSans } from "geist/font/sans";
import { GeistMono } from "geist/font/mono";
import { Analytics } from "@vercel/analytics/next";
import "@fontsource/playfair-display/500-italic.css";
import "@fontsource/playfair-display/600-italic.css";
import "@fontsource/playfair-display/500.css";
import "@fontsource/playfair-display/600.css";
import "@fontsource/lora/400.css";
import "@fontsource/lora/400-italic.css";
import "@fontsource/lora/500.css";
import "@fontsource/space-grotesk/500.css";
import "@fontsource/space-grotesk/600.css";
import "@fontsource/space-grotesk/700.css";
import "./globals.css";
import "./modes.css";

export const metadata: Metadata = {
  title: {
    default: "ial.chem — Edexcel International A Level Chemistry",
    template: "%s — ial.chem",
  },
  description:
    "Exam-focused notes for every Edexcel International A Level Chemistry topic (WCH11 + WCH12) — precise definitions, every equation, flashcards and a reading experience tuned to you.",
  keywords: [
    "Edexcel IAL Chemistry",
    "WCH11",
    "WCH12",
    "International A Level",
    "chemistry notes",
    "revision",
    "flashcards",
  ],
};

export const viewport: Viewport = {
  themeColor: "#111111",
};

// Applied before first paint so the saved theme never flashes.
const themeInit = `(function(){try{
var s=JSON.parse(localStorage.getItem("ialchem-settings")||"{}");
var st=s.state||{};
if(st.uiMode==="scholar"){var _tb=(st.themeByMode||{}).terminal,_ab=(st.accentByMode||{}).terminal;st.uiMode="terminal";st.theme=_tb||"sepia";st.accent=_ab||"coral"}
var d=document.documentElement;
d.dataset.uimode=st.uiMode||"terminal";
d.dataset.theme=st.theme||"sepia";
d.dataset.accent=st.accent||"coral";
d.dataset.font=st.fontFamily||"sans";
d.dataset.motion=st.motion||"normal";
d.dataset.focusmode=st.focusMode?"on":"off";
var r=d.style;
if(st.fontSize!=null){r.setProperty("--content-fs",["15px","16px","17.5px","19px"][st.fontSize]||"16px")}
if(st.lineHeight!=null){r.setProperty("--content-lh",["1.5","1.65","1.8"][st.lineHeight]||"1.65")}
if(st.width!=null){r.setProperty("--content-max",st.width==="wide"?"840px":"720px")}
if(st.fontFamily==="serif"){r.setProperty("--font-read-face","Lora, Georgia, serif")}
else if(st.fontFamily==="mono"){r.setProperty("--font-read-face",'var(--font-geist-mono), ui-monospace, monospace')}
}catch(e){}})();`;

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <head>
        <script dangerouslySetInnerHTML={{ __html: themeInit }} />
      </head>
      <body className={`${GeistSans.variable} ${GeistMono.variable} antialiased`}>
        {children}
        <Analytics />
      </body>
    </html>
  );
}
