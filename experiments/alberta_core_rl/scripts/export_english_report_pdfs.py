#!/usr/bin/env python
from __future__ import annotations

import argparse
import json
import os
import re
import textwrap
from dataclasses import dataclass
from pathlib import Path

os.environ.setdefault("MPLCONFIGDIR", str(Path(__file__).resolve().parents[3] / ".mplconfig"))

import matplotlib

matplotlib.use("Agg")
from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from PIL import Image


PAGE_WIDTH = 8.27
PAGE_HEIGHT = 11.69
MARGIN = 0.65
FOOTER_Y = 0.32

IMAGE_RE = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
LIST_RE = re.compile(r"^(\s*)([-*+]|\d+\.)\s+(.*)$")


@dataclass
class RenderStats:
    pages: int = 0
    images: int = 0
    missing_images: int = 0
    source_lines: int = 0


class ReportPdfRenderer:
    def __init__(self, source: Path, output: Path):
        self.source = source
        self.output = output
        self.stats = RenderStats()
        self.pdf: PdfPages | None = None
        self.fig = None
        self.y = PAGE_HEIGHT - MARGIN

    def render(self) -> RenderStats:
        self.output.parent.mkdir(parents=True, exist_ok=True)
        lines = self.source.read_text(encoding="utf-8").splitlines()
        self.stats.source_lines = len(lines)
        with PdfPages(self.output) as pdf:
            self.pdf = pdf
            self._new_page()
            self._parse(lines)
            self._save_page()
        return self.stats

    def _new_page(self) -> None:
        if self.fig is not None:
            self._save_page()
        self.fig = plt.figure(figsize=(PAGE_WIDTH, PAGE_HEIGHT), dpi=160)
        self.fig.patch.set_facecolor("white")
        self.y = PAGE_HEIGHT - MARGIN
        self.stats.pages += 1
        footer = f"{self.source.relative_to(Path.cwd())} | page {self.stats.pages}"
        self.fig.text(0.5, FOOTER_Y / PAGE_HEIGHT, footer, ha="center", va="bottom", fontsize=7, color="#666666")

    def _save_page(self) -> None:
        if self.fig is None or self.pdf is None:
            return
        self.pdf.savefig(self.fig)
        plt.close(self.fig)
        self.fig = None

    def _parse(self, lines: list[str]) -> None:
        paragraph: list[str] = []
        code: list[str] = []
        in_code = False

        def flush_paragraph() -> None:
            nonlocal paragraph
            if paragraph:
                self.add_paragraph(" ".join(part.strip() for part in paragraph if part.strip()))
                paragraph = []

        def flush_code() -> None:
            nonlocal code
            if code:
                self.add_code(code)
                code = []

        for raw in lines:
            line = raw.rstrip()
            if line.startswith("```"):
                if in_code:
                    flush_code()
                    in_code = False
                else:
                    flush_paragraph()
                    in_code = True
                continue
            if in_code:
                code.append(line)
                continue
            if not line.strip():
                flush_paragraph()
                self.add_space(0.08)
                continue
            image_match = IMAGE_RE.search(line)
            if image_match:
                flush_paragraph()
                self.add_image(image_match.group(2), image_match.group(1))
                continue
            heading = HEADING_RE.match(line)
            if heading:
                flush_paragraph()
                level = len(heading.group(1))
                self.add_heading(clean_inline(heading.group(2)), level)
                continue
            item = LIST_RE.match(line)
            if item:
                flush_paragraph()
                indent = min(0.45, 0.12 * (len(item.group(1)) // 2))
                self.add_paragraph(f"{item.group(2)} {clean_inline(item.group(3))}", bullet=True, indent=indent)
                continue
            if line.lstrip().startswith("|"):
                flush_paragraph()
                self.add_code([line])
                continue
            paragraph.append(line)

        flush_paragraph()
        flush_code()

    def add_heading(self, text: str, level: int) -> None:
        sizes = {1: 20, 2: 15, 3: 12, 4: 10}
        size = sizes.get(level, 9)
        weight = "bold" if level <= 3 else "semibold"
        self.add_space(0.10 if level <= 2 else 0.04)
        self._write_wrapped(text, size=size, weight=weight, color="#111111", line_gap=1.25)
        self.add_space(0.08 if level <= 2 else 0.04)

    def add_paragraph(self, text: str, bullet: bool = False, indent: float = 0.0) -> None:
        text = clean_inline(text)
        if not text:
            return
        prefix = "" if not bullet else "• "
        self._write_wrapped(prefix + text, size=9.2, indent=indent, line_gap=1.32)
        self.add_space(0.045)

    def add_code(self, lines: list[str]) -> None:
        for line in lines:
            self._write_wrapped(line if line else " ", size=7.3, family="monospace", color="#222222", line_gap=1.18)
        self.add_space(0.06)

    def add_image(self, target: str, alt: str) -> None:
        image_path = resolve_markdown_path(self.source, target)
        caption = clean_inline(alt)
        if not image_path.exists():
            self.stats.missing_images += 1
            self._write_wrapped(f"[missing image: {target}]", size=8.5, color="#9a3412", line_gap=1.2)
            return
        with Image.open(image_path) as img:
            img = img.convert("RGB")
            width_px, height_px = img.size
            usable_width = PAGE_WIDTH - 2 * MARGIN
            max_height = PAGE_HEIGHT * 0.46
            width = usable_width
            height = width * height_px / max(1, width_px)
            if height > max_height:
                height = max_height
                width = height * width_px / max(1, height_px)
            block_height = height + (0.30 if caption else 0.10)
            self._ensure_space(block_height)
            x = MARGIN + (usable_width - width) / 2.0
            y0 = self.y - height
            ax = self.fig.add_axes([x / PAGE_WIDTH, y0 / PAGE_HEIGHT, width / PAGE_WIDTH, height / PAGE_HEIGHT])
            ax.imshow(img)
            ax.axis("off")
            self.y = y0 - 0.08
            self.stats.images += 1
            if caption:
                self._write_wrapped(caption, size=8.0, color="#444444", line_gap=1.2)
            self.add_space(0.08)

    def add_space(self, amount: float) -> None:
        self.y -= amount
        if self.y < MARGIN:
            self._new_page()

    def _write_wrapped(
        self,
        text: str,
        size: float,
        weight: str = "normal",
        family: str = "DejaVu Sans",
        color: str = "#222222",
        indent: float = 0.0,
        line_gap: float = 1.28,
    ) -> None:
        available_width = PAGE_WIDTH - 2 * MARGIN - indent
        chars = max(28, int(available_width * 12.0 * 9.2 / size))
        wrapper = textwrap.TextWrapper(width=chars, replace_whitespace=False, break_long_words=True)
        lines = wrapper.wrap(text) or [""]
        line_height = size / 72.0 * line_gap
        for line in lines:
            self._ensure_space(line_height)
            self.fig.text(
                (MARGIN + indent) / PAGE_WIDTH,
                self.y / PAGE_HEIGHT,
                line,
                ha="left",
                va="top",
                fontsize=size,
                fontweight=weight,
                fontfamily=family,
                color=color,
            )
            self.y -= line_height

    def _ensure_space(self, height: float) -> None:
        if self.y - height < MARGIN:
            self._new_page()


def clean_inline(text: str) -> str:
    text = LINK_RE.sub(lambda m: f"{m.group(1)} ({m.group(2)})", text)
    text = text.replace("`", "")
    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("\\_", "_")
    return text.strip()


def resolve_markdown_path(source: Path, target: str) -> Path:
    target = target.split("#", 1)[0]
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    path = Path(target)
    if path.is_absolute():
        return path
    return (source.parent / path).resolve()


def collect_reports(root: Path) -> list[Path]:
    reports = []
    for path in sorted(root.rglob("report.md")):
        parts = set(path.parts)
        if "archive" in parts or path.name.endswith("_zh.md"):
            continue
        reports.append(path)
    return reports


def output_for(source: Path, final_root: Path, output_root: Path) -> Path:
    if output_root == Path():
        return source.with_suffix(".pdf")
    relative = source.relative_to(final_root)
    return output_root / relative.with_suffix(".pdf")


def main() -> None:
    parser = argparse.ArgumentParser(description="Export English final report Markdown files to lightweight PDFs.")
    parser.add_argument("--final-root", default="final")
    parser.add_argument("--reports-root", default="final/reports")
    parser.add_argument(
        "--output-root",
        default=None,
        help="Optional centralized PDF root. By default each report.pdf is written beside its report.md.",
    )
    parser.add_argument("--manifest", default="final/indexes/english_report_pdf_manifest.json")
    parser.add_argument("--only", nargs="*", default=None, help="Optional report.md paths to export.")
    args = parser.parse_args()

    final_root = Path(args.final_root).resolve()
    reports_root = Path(args.reports_root).resolve()
    output_root = Path(args.output_root).resolve() if args.output_root else Path()
    sources = [Path(p).resolve() for p in args.only] if args.only else collect_reports(reports_root)
    manifest = []
    for source in sources:
        if source.name != "report.md" or source.name.endswith("_zh.md"):
            continue
        output = output_for(source, final_root, output_root)
        stats = ReportPdfRenderer(source, output).render()
        manifest.append(
            {
                "source": str(source.relative_to(final_root.parent)),
                "pdf": str(output.relative_to(final_root.parent)),
                "pages": stats.pages,
                "images": stats.images,
                "missing_images": stats.missing_images,
                "source_lines": stats.source_lines,
            }
        )
        print(f"wrote {output} pages={stats.pages} images={stats.images} missing_images={stats.missing_images}")

    manifest_path = Path(args.manifest).resolve()
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {manifest_path}")


if __name__ == "__main__":
    main()
