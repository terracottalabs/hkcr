import type { LocalCompany, ForeignCompany } from "./types";

function truncate(str: string, len: number): string {
  if (!str) return "";
  return str.length > len ? str.slice(0, len - 1) + "…" : str;
}

function padRight(str: string, len: number): string {
  const s = str || "";
  return s.length >= len ? s.slice(0, len) : s + " ".repeat(len - s.length);
}

export function formatLocalTable(companies: LocalCompany[]): string {
  if (!companies.length) return "No results found.";

  const cols = [
    { key: "Brn", header: "BRN", width: 12 },
    { key: "English_Company_Name", header: "English Name", width: 40 },
    { key: "Chinese_Company_Name", header: "Chinese Name", width: 20 },
    { key: "Company_Type", header: "Type", width: 20 },
    { key: "Date_of_Incorporation", header: "Incorporated", width: 12 },
  ] as const;

  const header = cols.map((c) => padRight(c.header, c.width)).join(" │ ");
  const divider = cols.map((c) => "─".repeat(c.width)).join("─┼─");

  const rows = companies.map((co) =>
    cols.map((c) => padRight(truncate((co as Record<string, string>)[c.key], c.width), c.width)).join(" │ ")
  );

  return [header, divider, ...rows].join("\n");
}

export function formatForeignTable(companies: ForeignCompany[]): string {
  if (!companies.length) return "No results found.";

  const cols = [
    { key: "Brn", header: "BRN", width: 12 },
    { key: "Corporate_Name", header: "Corporate Name", width: 35 },
    { key: "Approved_name_for_carrying_on_business_in_H.K._Corporate", header: "HK Name", width: 25 },
    { key: "Place_of_Incorporation", header: "Origin", width: 15 },
    { key: "Date_of_Registration", header: "Registered", width: 12 },
  ] as const;

  const header = cols.map((c) => padRight(c.header, c.width)).join(" │ ");
  const divider = cols.map((c) => "─".repeat(c.width)).join("─┼─");

  const rows = companies.map((co) =>
    cols.map((c) => padRight(truncate((co as Record<string, string>)[c.key], c.width), c.width)).join(" │ ")
  );

  return [header, divider, ...rows].join("\n");
}

export function formatJson(data: unknown): string {
  return JSON.stringify(data, null, 2);
}
