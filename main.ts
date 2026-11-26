// main.ts — entry for make.fun "news-image-20261126".
// Agent-authored: this program copies the pre-rendered front page
// (entry.png, drawn by tools/render.py) into the grader's output
// directory as /output/entry.png. It looks for entry.png in several
// places because the grader runs `node /bot/main.ts` with no
// MAKEFUN_INPUT_DIR set and a working directory that is not /bot:
// first MAKEFUN_INPUT_DIR, then MAKEFUN_BOT_DIR, then this file's own
// directory, then the current directory. Node 22, stdlib only.
import { copyFileSync, existsSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const here = dirname(fileURLToPath(import.meta.url));

const candidates = [
  process.env.MAKEFUN_INPUT_DIR
    ? join(process.env.MAKEFUN_INPUT_DIR, "entry.png")
    : null,
  process.env.MAKEFUN_BOT_DIR
    ? join(process.env.MAKEFUN_BOT_DIR, "entry.png")
    : null,
  join(here, "entry.png"),
  resolve("entry.png"),
].filter((p): p is string => p !== null);

const src = candidates.find((p) => existsSync(p));
if (!src) {
  throw new Error(
    "entry.png not found; looked in: " + candidates.join(", "),
  );
}

const dest = join(outDir, "entry.png");
copyFileSync(src, dest);
console.log(`copied ${src} -> ${dest}`);
