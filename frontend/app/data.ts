export const apiBase = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";
export const apiKey = process.env.NEXT_PUBLIC_API_KEY ?? "dev-api-key";

export const dashboardCards = [
  {
    title: "Trending Developments",
    value: "Supreme Court insolvency threshold rulings",
    detail: "Metadata-only legal event clustering with official-source checks.",
  },
  {
    title: "Judge Analytics",
    value: "Bench patterns on commercial and transport disputes",
    detail: "Surface courts, judges, and treatment chains from retrieved authorities.",
  },
  {
    title: "Statute Activity",
    value: "IBC + Motor Vehicles Act references",
    detail: "Monitor statute mentions across judgments, chunks, and alerts.",
  },
];
