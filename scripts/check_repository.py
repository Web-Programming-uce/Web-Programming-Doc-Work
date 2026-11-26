#!/usr/bin/env python3
"""Dependency-free, bootstrap-time validation. NOT an implementation test suite."""
from pathlib import Path
import re
import sys

# Double-encoded UTF-8 ("mojibake") such as â€”, â€“, â†’, Â· or Ã³.
# Markdown files must contain the intended characters (—, –, →, ·, ó), not their CP1252 misreadings.
MOJIBAKE = re.compile(
    '\u00e2[\u0080-\u00bf\u2018-\u203a\u20ac\u2122\u0152\u0153\u0160\u0161\u0178\u017d\u017e\u0192\u02c6\u02dc]{1,2}'
    '|\u00c2[\u0080-\u00bf]'
    '|\u00c3[\u0080-\u00bf]'
)

repo = Path(__file__).resolve().parents[1]
required = [
    'README.md', 'CONTRIBUTING.md', 'AGENTS.md',
    '.editorconfig', '.gitignore',
    '.github/pull_request_template.md',
    '.github/workflows/repository-checks.yml',
    'docs/requirements/SkillCheck_Master_Specification.md',
    'docs/requirements/README.md',
    'docs/sprint-1/README.md',
    'docs/workflow/GIT_WORKFLOW.md',
    'docs/workflow/REPOSITORY_BOOTSTRAP.md',
    'docs/decisions/README.md',
    'docs/decisions/ADR-0001-proposed-architecture-and-workflow.md',
    'docs/architecture/README.md',
    'apps/api/README.md', 'apps/web/README.md', 'apps/site/README.md',
    'apps/mobile/README.md', 'apps/desktop/README.md',
    'packages/shared/README.md', 'packages/ui/README.md',
    'infra/README.md', 'tests/README.md',
]
figures = [
    'docs/sprint-1/figures/WP20_Context.svg',
    'docs/sprint-1/figures/WP20_Containers.svg',
    'docs/sprint-1/figures/WP20_Speech_Sequence.svg',
    'docs/sprint-1/figures/WP20_RAG_Sequence.svg',
    'docs/sprint-1/figures/WP20_Deployment.svg',
    'docs/sprint-1/figures/WP30_Evaluation.svg',
    'docs/sprint-1/figures/WP30_RAG.svg',
    'docs/sprint-1/figures/WP31_Security_Boundaries.svg',
]
required.extend(figures)
for key in ('WP-20', 'WP-21', 'WP-30', 'WP-31'):
    required.extend(str(x.relative_to(repo)) for x in (repo / 'docs/sprint-1').glob(f'{key}_*.md'))
    required.extend(str(x.relative_to(repo)) for x in (repo / 'docs/sprint-1').glob(f'{key}_*.pdf'))

errors = []
for relative in required:
    path = repo / relative
    if not path.is_file() or path.stat().st_size < 10:
        errors.append(f'Missing or empty file: {relative}')

for key in ('WP-20', 'WP-21', 'WP-30', 'WP-31'):
    files = list((repo / 'docs/sprint-1').glob(f'{key}_*.md'))
    if len(files) != 1:
        errors.append(f'Expected exactly one Markdown document for {key}, found {len(files)}')
    pdfs = list((repo / 'docs/sprint-1').glob(f'{key}_*.pdf'))
    if len(pdfs) != 1:
        errors.append(f'Expected exactly one PDF for {key}, found {len(pdfs)}')

master_path = repo / 'docs/requirements/SkillCheck_Master_Specification.md'
if master_path.is_file():
    master = master_path.read_text(encoding='utf-8')
    for n in range(1, 27):
        marker = f'R{n:02d}'
        if marker not in master:
            errors.append(f'Master Specification missing {marker}')
    if 'OPT-01' not in master:
        errors.append('Master Specification missing OPT-01')
    if 'https://github.com/Web-Programming-uce/Web-Programming-Doc-Work' not in master:
        errors.append('Master Specification missing official repo URL')

# Every diagram must be linked from at least one Markdown document (no orphan figures).
markdown_text = '\n'.join(
    path.read_text(encoding='utf-8', errors='replace')
    for path in repo.glob('docs/**/*.md')
)
for figure in figures:
    if Path(figure).name not in markdown_text:
        errors.append(f'Diagram not linked from any Markdown document: {figure}')

# Markdown encoding: valid UTF-8 without BOM and without double-encoded (mojibake) characters.
for path in sorted(repo.rglob('*.md')):
    if any(part in {'.git', 'node_modules'} for part in path.parts):
        continue
    relative = path.relative_to(repo)
    raw = path.read_bytes()
    if raw.startswith(b'\xef\xbb\xbf'):
        errors.append(f'UTF-8 BOM not allowed: {relative}')
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError as exc:
        errors.append(f'Invalid UTF-8: {relative} ({exc.reason})')
        continue
    for match in MOJIBAKE.finditer(text):
        line = text.count('\n', 0, match.start()) + 1
        errors.append(f'Mojibake (double-encoded UTF-8) at {relative}:{line}: {match.group(0)!r}')

for suffix in ('.env', '.pem', '.key', '.p12'):
    for file in repo.rglob(f'*{suffix}'):
        if any(p in {'.git', 'node_modules'} for p in file.parts):
            continue
        errors.append(f'Potential private file in package: {file.relative_to(repo)}')

if errors:
    print('Repository baseline FAILED:')
    for error in errors:
        print(f' - {error}')
    sys.exit(1)

print(f'Repository baseline passed: {len(required)} required files checked; master requirements R01-R26 and OPT-01 present.')
print('Markdown encoding checked: valid UTF-8, no BOM and no mojibake sequences.')
print('NOTE: No application build, functional test, security scan or deployment was executed by this check.')
