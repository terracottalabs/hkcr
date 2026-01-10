#!/usr/bin/env bun
import { searchLocal, searchForeign } from "./api";
import { formatLocalTable, formatForeignTable, formatJson } from "./format";

const HELP = `
hkcr - Hong Kong Companies Registry Search

Usage: hkcr [options] <query>

Options:
  -f, --foreign   Search non-HK companies (default: local)
  -b, --brn       Search by Business Registration Number
  -e, --exact     Exact match (default: begins_with for names)
  -j, --json      Output as JSON (default: table)
  -h, --help      Show this help

Examples:
  hkcr "China"           Search local companies starting with "China"
  hkcr -f "China"        Search foreign companies
  hkcr -b C1572528       Search by BRN
  hkcr "China" -j        Output as JSON
`.trim();

interface Options {
  foreign: boolean;
  brn: boolean;
  exact: boolean;
  json: boolean;
  help: boolean;
}

function parseArgs(args: string[]): { options: Options; query: string } {
  const options: Options = { foreign: false, brn: false, exact: false, json: false, help: false };
  const positional: string[] = [];

  for (const arg of args) {
    if (arg === "-f" || arg === "--foreign") options.foreign = true;
    else if (arg === "-b" || arg === "--brn") options.brn = true;
    else if (arg === "-e" || arg === "--exact") options.exact = true;
    else if (arg === "-j" || arg === "--json") options.json = true;
    else if (arg === "-h" || arg === "--help") options.help = true;
    else if (!arg.startsWith("-")) positional.push(arg);
  }

  return { options, query: positional.join(" ") };
}

async function main() {
  const { options, query } = parseArgs(Bun.argv.slice(2));

  if (options.help || !query) {
    console.log(HELP);
    process.exit(options.help ? 0 : 1);
  }

  try {
    const params = { query, byBrn: options.brn, exact: options.exact };

    if (options.foreign) {
      const results = await searchForeign(params);
      console.log(options.json ? formatJson(results) : formatForeignTable(results));
    } else {
      const results = await searchLocal(params);
      console.log(options.json ? formatJson(results) : formatLocalTable(results));
    }
  } catch (err) {
    console.error("Error:", err instanceof Error ? err.message : err);
    process.exit(1);
  }
}

main();
