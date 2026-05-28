from pathlib import Path
import textwrap

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Circle, Polygon


plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman", "Times", "Nimbus Roman", "DejaVu Serif"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["font.size"] = 7.2


COLORS = {
    "gold": "#FFD23F",
    "gold_light": "#FFF3B8",
    "blue": "#5B9BD5",
    "blue_light": "#DDEBF7",
    "green": "#70AD47",
    "green_light": "#E2F0D9",
    "teal": "#55B7A6",
    "teal_light": "#D9F0EC",
    "violet": "#8E7CC3",
    "violet_light": "#E7E1F5",
    "gray": "#8A8A8A",
    "dark": "#263238",
    "line": "#3A3A3A",
    "panel": "#F7F8FA",
}


def save_figure(fig, out_path):
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "svg", "png"):
        fig.savefig(out_path.with_suffix(f".{ext}"), dpi=600, bbox_inches="tight", pad_inches=0.02)
    plt.close(fig)


def rounded_box(ax, x, y, w, h, fc, ec="#3A3A3A", lw=0.9, radius=0.055, zorder=1):
    patch = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle=f"round,pad=0.012,rounding_size={radius}",
        facecolor=fc,
        edgecolor=ec,
        linewidth=lw,
        zorder=zorder,
    )
    ax.add_patch(patch)
    return patch


def wrapped_text(ax, x, y, text, width=20, **kwargs):
    ax.text(x, y, "\n".join(textwrap.wrap(text, width=width, break_long_words=False)), **kwargs)


def draw_icon(ax, cx, cy, kind, color):
    if kind == "grid":
        size = 0.16
        for i in range(2):
            for j in range(2):
                rounded_box(ax, cx - 0.18 + j * 0.19, cy - 0.18 + i * 0.19, size, size, "#FFFFFF", color, lw=0.8, radius=0.018, zorder=4)
    elif kind == "text":
        ax.text(cx, cy, "T", ha="center", va="center", fontsize=10.5, fontweight="bold", color=color, zorder=5)
        ax.plot([cx - 0.16, cx + 0.16], [cy - 0.18, cy - 0.18], color=color, lw=1.0, zorder=4)
    elif kind == "mask":
        verts = [(cx - 0.18, cy - 0.08), (cx - 0.08, cy + 0.16), (cx + 0.16, cy + 0.11), (cx + 0.20, cy - 0.10), (cx + 0.02, cy - 0.20)]
        ax.add_patch(Polygon(verts, closed=True, facecolor="#FFFFFF", edgecolor=color, linewidth=1.0, zorder=4))
        ax.add_patch(Circle((cx + 0.04, cy + 0.01), 0.05, facecolor=color, edgecolor=color, zorder=5))
    elif kind == "reason":
        ax.add_patch(Circle((cx - 0.06, cy + 0.02), 0.15, facecolor="#FFFFFF", edgecolor=color, linewidth=1.0, zorder=4))
        for dx, dy in [(-0.10, 0.04), (-0.02, 0.08), (0.06, 0.02)]:
            ax.add_patch(Circle((cx + dx, cy + dy), 0.025, facecolor=color, edgecolor=color, zorder=5))
        ax.plot([cx + 0.06, cx + 0.18], [cy - 0.10, cy - 0.20], color=color, lw=1.0, zorder=4)


def draw_card(ax, x, y, w, h, title, badge, rows, color, light_color, icon):
    rounded_box(ax, x, y, w, h, "#FFFFFF", ec="#D6DADF", lw=0.9, radius=0.07, zorder=1)
    rounded_box(ax, x + 0.05, y + h - 0.72, w - 0.10, 0.62, light_color, ec="none", lw=0, radius=0.055, zorder=2)
    draw_icon(ax, x + 0.34, y + h - 0.42, icon, color)
    wrapped_text(ax, x + 0.64, y + h - 0.34, title, width=18, ha="left", va="center", fontsize=8.0, fontweight="bold", color=COLORS["dark"], linespacing=0.95, zorder=5)
    rounded_box(ax, x + 0.64, y + h - 0.68, w - 0.80, 0.18, "#FFFFFF", ec="none", lw=0, radius=0.02, zorder=3)
    ax.text(x + 0.72, y + h - 0.59, badge, ha="left", va="center", fontsize=5.7, color=color, fontstyle="italic", zorder=5)

    row_y = [y + 1.30, y + 0.76, y + 0.22]
    row_labels = ["Input", "Core", "Output"]
    for idx, (label, text) in enumerate(zip(row_labels, rows)):
        rounded_box(ax, x + 0.14, row_y[idx], w - 0.28, 0.42, COLORS["panel"], ec="#E4E7EB", lw=0.6, radius=0.035, zorder=2)
        ax.text(x + 0.27, row_y[idx] + 0.30, label, ha="left", va="center", fontsize=5.0, color=color, fontweight="bold", zorder=5)
        wrapped_text(ax, x + w / 2, row_y[idx] + 0.13, text, width=24, ha="center", va="center", fontsize=5.75, color=COLORS["dark"], linespacing=0.95, zorder=5)


def make_figure(out_dir):
    fig, ax = plt.subplots(figsize=(7.35, 3.30))
    ax.set_xlim(0, 12.7)
    ax.set_ylim(0, 4.15)
    ax.axis("off")

    ax.text(
        0.15,
        3.98,
        "Foundation paradigms",
        ha="left",
        va="center",
        fontsize=10.0,
        fontweight="bold",
        color=COLORS["dark"],
    )
    ax.text(
        12.55,
        3.98,
        "fixed labels  ->  text vocabulary  ->  prompted masks  ->  implicit intent",
        ha="right",
        va="center",
        fontsize=6.3,
        color="#586069",
        fontstyle="italic",
    )

    ax.add_patch(
        FancyArrowPatch(
            (0.32, 3.62),
            (12.34, 3.62),
            arrowstyle="-|>",
            mutation_scale=12,
            linewidth=1.1,
            color="#B8C0CC",
            zorder=0,
        )
    )
    stage_x = [0.35, 3.48, 6.61, 9.74]
    stage_labels = ["fixed labels", "text vocabulary", "prompted masks", "implicit intent"]
    for i, (x, label) in enumerate(zip(stage_x, stage_labels), start=1):
        ax.add_patch(Circle((x + 1.14, 3.62), 0.115, facecolor="white", edgecolor="#B8C0CC", linewidth=1.0, zorder=3))
        ax.text(x + 1.14, 3.62, str(i), ha="center", va="center", fontsize=5.9, fontweight="bold", color="#6B7280", zorder=4)
        ax.text(x + 1.14, 3.39, label, ha="center", va="center", fontsize=6.2, color="#6B7280", zorder=4)

    cards = [
        (
            "Closed-set\nsegmentation",
            "predefined labels",
            ["image + labels", "pixel classifier", "class mask"],
            COLORS["gray"],
            "#ECEFF1",
            "grid",
        ),
        (
            "Open-vocabulary\nsegmentation",
            "text-defined labels",
            ["image + text labels", "dense V-L alignment", "open-vocab mask"],
            COLORS["blue"],
            COLORS["blue_light"],
            "text",
        ),
        (
            "Promptable\nsegmentation",
            "mask prior + grounding",
            ["image + prompt", "mask prior + grounding", "grounded mask"],
            COLORS["green"],
            COLORS["green_light"],
            "mask",
        ),
        (
            "Reasoning\nsegmentation",
            "infer target first",
            ["image + instruction", "reasoning + decoder", "rationale + mask"],
            COLORS["violet"],
            COLORS["violet_light"],
            "reason",
        ),
    ]

    for x, card in zip(stage_x, cards):
        draw_card(ax, x, 0.28, 2.72, 2.82, *card)

    for x in [3.14, 6.27, 9.40]:
        ax.add_patch(
            FancyArrowPatch(
                (x, 1.74),
                (x + 0.25, 1.74),
                arrowstyle="-|>",
                mutation_scale=10,
                linewidth=1.0,
                color="#667085",
                zorder=5,
            )
        )

    save_figure(fig, Path(out_dir) / "foundation_paradigms")


def main():
    root = Path(__file__).resolve().parents[2]
    out_dir = root / "Fig"
    make_figure(out_dir)
    print(f"Saved foundation paradigm figure to {out_dir}")


if __name__ == "__main__":
    main()
