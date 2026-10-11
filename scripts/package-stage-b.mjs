import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { execSync } from 'node:child_process';

const ROOT = process.cwd();
const STAGING = path.join(ROOT, 'tmp', 'stage-b-package');
const PACKAGE_DIR = path.join(STAGING, 'gate-pyq-stage-b-verification');
const ZIP_NAME = 'gate-pyq-stage-b-verification.zip';
const ZIP_ROOT = path.join(ROOT, ZIP_NAME);
const DESKTOP_PATH = 'C:/Users/godbe/Desktop/' + ZIP_NAME;

console.log('--- PACKAGING STAGE B VERIFICATION ARCHIVE ---');

// Clean and recreate staging
if (fs.existsSync(STAGING)) {
  fs.rmSync(STAGING, { recursive: true, force: true });
}
fs.mkdirSync(PACKAGE_DIR, { recursive: true });

function copyFileSafe(srcRel, dstRel) {
  const src = path.join(ROOT, srcRel);
  const dst = path.join(PACKAGE_DIR, dstRel || srcRel);
  if (!fs.existsSync(src)) return;
  fs.mkdirSync(path.dirname(dst), { recursive: true });
  fs.copyFileSync(src, dst);
}

function copyDirSafe(dirRel) {
  const srcDir = path.join(ROOT, dirRel);
  if (!fs.existsSync(srcDir)) return;
  const entries = fs.readdirSync(srcDir, { withFileTypes: true });
  for (const entry of entries) {
    const rel = path.join(dirRel, entry.name).replace(/\\/g, '/');
    if (['node_modules', '.git', 'tmp', 'scratch'].some(ign => rel.includes(ign))) continue;
    if (entry.isDirectory()) {
      copyDirSafe(rel);
    } else {
      copyFileSafe(rel);
    }
  }
}

// 1. Core Web Root Files
const rootFiles = [
  'index.html',
  'manifest.webmanifest',
  'sw.js',
  'package.json',
  'package-lock.json',
  'README.md',
  'STAGE_B_STABILIZATION_REPORT.md',
  'STABILIZATION_SPRINT_TRACKER.md',
  'CONTENT_QUALITY_AUDIT.md',
  'MATH_NOTATION_INVENTORY.md',
  'REMAINING_ISSUES.md',
  'MANUAL_REVIEW_CHECKLIST.md'
];

for (const file of rootFiles) copyFileSafe(file);

// 2. Directories
copyDirSafe('js');
copyDirSafe('css');
copyDirSafe('assets');
copyDirSafe('data');
copyDirSafe('figures');
copyDirSafe('tests');
copyDirSafe('.github');
copyDirSafe('docs');
copyDirSafe('Aptitude Sets');
copyDirSafe('internal');

// 3. Essential Scripts
const essentialScripts = [
  'scripts/serve.mjs',
  'scripts/serve-forensic.mjs',
  'scripts/check.mjs',
  'scripts/validate-data.mjs',
  'scripts/validate-ae.mjs'
];
for (const s of essentialScripts) copyFileSafe(s);

// Count files in package
let packagedFiles = 0;
let totalBytes = 0;
function countDir(d) {
  for (const f of fs.readdirSync(d, { withFileTypes: true })) {
    const full = path.join(d, f.name);
    if (f.isDirectory()) {
      countDir(full);
    } else {
      packagedFiles++;
      totalBytes += fs.statSync(full).size;
    }
  }
}
countDir(PACKAGE_DIR);

console.log(`Staged ${packagedFiles} files (${(totalBytes / (1024 * 1024)).toFixed(2)} MB uncompressed).`);

// 4. Create ZIP archive using tar (built-in Windows 10/11) or Compress-Archive
console.log('Compressing into ZIP archive...');
if (fs.existsSync(ZIP_ROOT)) fs.unlinkSync(ZIP_ROOT);

try {
  execSync(`tar -a -cf "${ZIP_ROOT}" -C "${STAGING}" gate-pyq-stage-b-verification`, { stdio: 'inherit' });
} catch (e) {
  const psCommand = `Compress-Archive -Path '${PACKAGE_DIR}/*' -DestinationPath '${ZIP_ROOT}' -Force`;
  execSync(`powershell -NoProfile -Command "${psCommand}"`, { stdio: 'inherit' });
}

const zipStats = fs.statSync(ZIP_ROOT);
const hash = crypto.createHash('sha256').update(fs.readFileSync(ZIP_ROOT)).digest('hex');

console.log(`Created ${ZIP_ROOT}`);
console.log(`Size: ${(zipStats.size / (1024 * 1024)).toFixed(2)} MB (${zipStats.size} bytes)`);
console.log(`SHA256: ${hash}`);

// 5. Copy to user Desktop
try {
  fs.copyFileSync(ZIP_ROOT, DESKTOP_PATH);
  console.log(`Successfully copied to Desktop: ${DESKTOP_PATH}`);
} catch (err) {
  console.warn(`Could not copy to Desktop: ${err.message}`);
}

console.log('--- PACKAGING COMPLETE ---');
