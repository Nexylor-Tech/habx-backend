import { GoogleGenAI } from "@google/genai";

const ai = new GoogleGenAI({});

export async function useGemini(contents: string) {
  const result = await ai.models.generateContent({
    model: "gemini-2.5-flash-lite",
    contents
  });
  return result.text
}
