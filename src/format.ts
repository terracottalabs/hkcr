import type { LocalCompany, ForeignCompany } from "./types";

// Get display width accounting for CJK characters (which are double-width)
function displayWidth(str: string): number {
  let width = 0;
  for (const char of str) {
    const code = char.codePointAt(0) ?? 0;
    // CJK ranges: Chinese, Japanese, Korean characters are double-width
    if (
      (code >= 0x4e00 && code <= 0x9fff) || // CJK Unified Ideographs
      (code >= 0x3400 && code <= 0x4dbf) || // CJK Extension A
      (code >= 0x3000 && code <= 0x303f) || // CJK Punctuation
      (code >= 0xff00 && code <= 0xffef)    // Fullwidth forms
    ) {
      width += 2;
    } else {
      width += 1;
    }
  }
  return width;
}

function wrapText(str: string, width: number): string[] {
  if (!str) return [""];
  const words = str.split(" ");
  const lines: string[] = [];
  let current = "";
  let currentWidth = 0;

  for (const word of words) {
    const wordWidth = displayWidth(word);
    if (!current) {
      current = word;
      currentWidth = wordWidth;
    } else if (currentWidth + 1 + wordWidth <= width) {
      current += " " + word;
      currentWidth += 1 + wordWidth;
    } else {
      lines.push(current);
      current = word;
      currentWidth = wordWidth;
    }
  }
  if (current) lines.push(current);
  return lines.length ? lines : [""];
}

function padRight(str: string, targetWidth: number): string {
  const s = str || "";
  const currentWidth = displayWidth(s);
  if (currentWidth >= targetWidth) return s;
  return s + " ".repeat(targetWidth - currentWidth);
}

interface Column {
  key: string;
  header: string;
  width: number;
}

function formatTable<T>(companies: T[], cols: Column[]): string {
  if (!companies.length) return "No results found.";

  const header = cols.map((c) => padRight(c.header, c.width)).join(" │ ");
  const divider = cols.map((c) => "─".repeat(c.width)).join("─┼─");

  const rows: string[] = [];
  for (const co of companies) {
    const wrapped = cols.map((c) => wrapText((co as Record<string, string>)[c.key] || "", c.width));
    const maxLines = Math.max(...wrapped.map((w) => w.length));

    for (let i = 0; i < maxLines; i++) {
      const row = cols.map((_, j) => padRight(wrapped[j]?.[i] ?? "", cols[j].width)).join(" │ ");
      rows.push(row);
    }
  }

  return [header, divider, ...rows].join("\n");
}

export function formatLocalTable(companies: LocalCompany[]): string {
  return formatTable(companies, [
    { key: "Brn", header: "BRN", width: 10 },
    { key: "English_Company_Name", header: "English Name", width: 30 },
    { key: "Chinese_Company_Name", header: "Chinese Name", width: 16 },
    { key: "Company_Type", header: "Type", width: 18 },
    { key: "Date_of_Incorporation", header: "Incorporated", width: 12 },
  ]);
}

export function formatForeignTable(companies: ForeignCompany[]): string {
  return formatTable(companies, [
    { key: "Brn", header: "BRN", width: 10 },
    { key: "Corporate_Name", header: "Corporate Name", width: 30 },
    { key: "Approved_name_for_carrying_on_business_in_H.K._Corporate", header: "HK Name", width: 20 },
    { key: "Place_of_Incorporation", header: "Origin", width: 12 },
    { key: "Date_of_Registration", header: "Registered", width: 12 },
  ]);
}

export function formatJson(data: unknown): string {
  return JSON.stringify(data, null, 2);
}
