"""Measure how Claude talks in the transcripts on this machine.

Reads the JSONL transcripts Claude Code keeps under ~/.claude/projects and
reports, per skill, how long the replies to the user are and how often the
phrasing that STYLE.md bans shows up. Run it before and after a change to the
skills to see whether the change did anything.

    python scripts/measure-replies.py                  # every project
    python scripts/measure-replies.py --since 2026-09-01 c--Users-me-code-myrepo

A project argument is a directory name under ~/.claude/projects.
"""
import argparse
import collections
import glob
import json
import os
import re
import statistics

MANNERED = [
    "landmine", "load-bearing", "fold in", "folds in", "silently", "quietly", "the real question",
    "matters more than it looks", "worth noting", "in other words", "the key insight", "the story",
    "the picture", "say the word", "earns its keep", "north star", "table stakes", "blast radius",
    "footgun", "rabbit hole", "under the hood", "boils down", "the upshot", "in short", "genuinely",
    "honest", "truthful", "the fix is", "framing", "reframe", "lens", "tension", "friction", "surface",
    "no home", "the false promise", "for free", "pins", "strand",
]


def replies(project_dir, since):
    skill = None
    for path in glob.glob(os.path.join(project_dir, "*.jsonl")):
        with open(path, encoding="utf-8", errors="replace") as handle:
            for line in handle:
                try:
                    entry = json.loads(line)
                except ValueError:
                    continue
                message = entry.get("message") or {}
                content = message.get("content")
                if entry.get("type") == "user":
                    texts = [content] if isinstance(content, str) else [b.get("text", "") for b in content or [] if isinstance(b, dict)]
                    for text in texts:
                        match = re.search(r"<command-name>(/[\w:-]+)</command-name>", text or "")
                        if match:
                            skill = match.group(1)
                if entry.get("type") != "assistant" or entry.get("isSidechain") or not isinstance(content, list):
                    continue
                if since and entry.get("timestamp", "") < since:
                    continue
                for block in content:
                    if block.get("type") == "text" and block.get("text", "").strip():
                        yield skill or "(no skill)", block["text"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("projects", nargs="*", help="directory names under ~/.claude/projects (default: all)")
    parser.add_argument("--since", default="", help="ISO date; ignore replies before it")
    args = parser.parse_args()
    root = os.path.expanduser("~/.claude/projects")
    names = args.projects or sorted(os.listdir(root))

    by_skill = collections.defaultdict(list)
    hits = collections.Counter()
    words = dashes = bold = 0
    for name in names:
        for skill, text in replies(os.path.join(root, name), args.since):
            count = len(text.split())
            by_skill[skill].append(count)
            words += count
            dashes += text.count("—")
            bold += text.count("**") // 2
            lowered = text.lower()
            for phrase in MANNERED:
                hits[phrase] += lowered.count(phrase)

    total = sum(len(v) for v in by_skill.values())
    if not total:
        print("no replies found")
        return
    print(f"{total} replies, {words} words, {dashes / words * 1000:.1f} em-dashes per 1000 words, {bold} bold spans")
    print(f"\n{'skill':40} {'replies':>7} {'median':>6} {'p90':>5} {'>300w':>5}")
    for skill, counts in sorted(by_skill.items(), key=lambda item: -len(item[1])):
        ordered = sorted(counts)
        print(f"{skill:40} {len(counts):7d} {statistics.median(counts):6.0f} {ordered[int(len(ordered) * 0.9)]:5d} {sum(1 for c in counts if c > 300):5d}")
    print("\nmannered phrases:")
    for phrase, count in hits.most_common(15):
        if count:
            print(f"  {count:5d}  {phrase}")


if __name__ == "__main__":
    main()
