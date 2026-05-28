from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrow, FancyBboxPatch, PathPatch
from matplotlib.path import Path as MplPath

plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman", "Times", "Nimbus Roman", "DejaVu Serif"]
plt.rcParams["svg.fonttype"] = "none"
plt.rcParams["pdf.fonttype"] = 42
plt.rcParams["font.size"] = 8


COLORS = {
    "gold": "#FFD23F",
    "gold_light": "#FFE99A",
    "blue": "#5B9BD5",
    "blue_light": "#DDEBF7",
    "green": "#70AD47",
    "green_light": "#E2F0D9",
    "trunk": "#E5F2DD",
    "gray": "#8A8A8A",
    "black": "#000000",
    "root": "#E8E8E8",
    "box_green": "#E2F0D9",
}


def save_figure(fig, out_path):
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    for ext in ("pdf", "svg", "png"):
        fig.savefig(out_path.with_suffix(f".{ext}"), dpi=600, bbox_inches="tight")
    plt.close(fig)


def draw_arrow_axis(ax, y, color, label, milestones, descriptor, x_start=1.45, x_end=9.45):
    ax.add_patch(
        FancyArrow(
            x_start,
            y,
            x_end - x_start,
            0,
            width=0.34,
            head_width=0.74,
            head_length=0.42,
            length_includes_head=True,
            facecolor=color,
            edgecolor=color,
            linewidth=0,
            alpha=0.92,
        )
    )
    ax.text(
        x_start + 0.60,
        y + 0.47,
        label,
        ha="center",
        va="center",
        fontsize=9,
        fontstyle="italic",
        fontweight="bold",
        color="#6F5200" if color == COLORS["gold"] else "#1F4E79" if color == COLORS["blue"] else "#3B641F",
    )
    xs = [3.55, 5.05, 6.55, 8.05]
    for x, m in zip(xs, milestones):
        ax.scatter(
            [x],
            [y],
            s=210,
            facecolors="white",
            edgecolors=COLORS["gray"],
            linewidths=2.2,
            zorder=5,
        )
        ax.text(x, y + 0.58, m, ha="center", va="bottom", fontsize=8.5, fontweight="bold")
    ax.annotate(
        "",
        xy=(7.35, y - 0.57),
        xytext=(4.85, y - 0.57),
        arrowprops=dict(arrowstyle="->", linestyle="--", color="#5A4A18", lw=1.0),
    )
    left_text, right_text = descriptor
    ax.text(4.55, y - 0.57, left_text, ha="right", va="center", fontsize=8.5, fontstyle="italic", color="#5A4A18")
    ax.text(7.45, y - 0.57, right_text, ha="left", va="center", fontsize=8.5, fontstyle="italic", color="#5A4A18")


def make_fig3(out_dir):
    fig, ax = plt.subplots(figsize=(7.1, 3.95))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4.9)
    ax.axis("off")

    verts = [
        (1.38, 4.22),
        (0.98, 4.22),
        (0.98, 0.98),
        (1.38, 0.98),
    ]
    codes = [MplPath.MOVETO, MplPath.CURVE3, MplPath.CURVE3, MplPath.LINETO]
    trunk_path = MplPath(verts, codes)
    ax.add_patch(
        PathPatch(
            trunk_path,
            facecolor="none",
            edgecolor=COLORS["trunk"],
            linewidth=21,
            capstyle="round",
            joinstyle="round",
            zorder=0,
        )
    )
    ax.scatter([0.98], [2.62], s=210, facecolors="white", edgecolors=COLORS["gray"], linewidths=2.2, zorder=6)
    ax.text(0.26, 2.62, "Closed-set\nseg.", ha="center", va="center", fontsize=7.8, fontweight="bold")

    draw_arrow_axis(
        ax,
        4.18,
        COLORS["gold"],
        "Semantic\nSpace",
        ["OVSeg", "USE", "FineSem", "LangHop"],
        ("Fixed labels", "Language-defined vocabularies"),
    )
    draw_arrow_axis(
        ax,
        2.62,
        COLORS["blue"],
        "Segmentation\nFramework",
        ["CLIP", "SAM", "GLaMM", "LENS"],
        ("Separate recognizer/masker", "Unified or composed V-L system"),
    )
    draw_arrow_axis(
        ax,
        1.06,
        COLORS["green"],
        "Downstream\nTask",
        ["OVSS", "RES", "RIS", "3D/Video"],
        ("Category masks", "Reasoning and scenario grounding"),
    )

    save_figure(fig, Path(out_dir) / "background_development_axes")


def rounded_box(ax, x, y, w, h, text, fc, fontsize=8.2, lw=1.25, italic_lines=None, ha="center"):
    box = FancyBboxPatch(
        (x, y),
        w,
        h,
        boxstyle="round,pad=0.018,rounding_size=0.055",
        facecolor=fc,
        edgecolor="black",
        linewidth=lw,
    )
    ax.add_patch(box)
    if italic_lines:
        lines = text.split("\n")
        line_h = h / (len(lines) + 1)
        start_y = y + h - line_h * 0.75
        for i, line in enumerate(lines):
            style = "italic" if i in italic_lines else "normal"
            tx = x + 0.10 if ha == "left" else x + w / 2
            ax.text(tx, start_y - i * line_h, line, ha=ha, va="center", fontsize=fontsize, fontstyle=style)
    else:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fontsize, linespacing=1.25)
    return box


def connector(ax, x1, y1, x2, y2, arrow=True):
    props = dict(arrowstyle="-|>" if arrow else "-", color="black", lw=1.1, shrinkA=0, shrinkB=0, mutation_scale=7.5)
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=props)


def make_fig4(out_dir):
    fig, ax = plt.subplots(figsize=(11.2, 5.65))
    ax.set_xlim(0, 13.6)
    ax.set_ylim(0, 8)
    ax.axis("off")

    root_x, root_y, root_w, root_h = 4.15, 7.25, 5.3, 0.55
    rounded_box(
        ax,
        root_x,
        root_y,
        root_w,
        root_h,
        "Open-Vocabulary and Reasoning Segmentation\nwith Vision-Language Foundation Models",
        COLORS["root"],
        fontsize=8.3,
        lw=1.25,
    )

    col_x = [0.28, 3.68, 7.08, 10.48]
    col_w = 2.86
    top_y, top_h = 6.10, 0.70
    columns = [
        (
            "Open-Vocabulary Segmentation\n(Sec. 5)",
            [
                "CLIP Dense Alignment (Sec. 5.1)\n• pixel V-L alignment\n• feature purification\n• label-free semantics",
                "Proposal/Mask Classification (Sec. 5.2)\n• proposal classification\n• segment embeddings\n• mask semantic assignment",
                "Efficient/Fine-grained OV Seg. (Sec. 5.3)\n• part segmentation\n• efficient adaptation\n• training-free routes",
            ],
        ),
        (
            "Promptable and Grounded Segmentation\n(Sec. 6)",
            [
                "SAM/SAM2 Mask Priors (Sec. 6.1)\n• prompt-conditioned masks\n• class-agnostic priors\n• OV composition",
                "Region/Mask-Text Grounding (Sec. 6.2)\n• phrase-region matching\n• referring segmentation\n• grounded dialogue",
                "Prompt Learning and Adapters (Sec. 6.3)\n• text/visual prompts\n• feature adapters\n• training-free composition",
            ],
        ),
        (
            "Reasoning Segmentation\n(Sec. 7)",
            [
                "MLLM-guided Segmentation (Sec. 7.1)\n• segmentation tokens\n• pixel decoders\n• grounded conversation",
                "Reasoning-to-Mask (Sec. 7.2)\n• implicit targets\n• multi-step instructions\n• rule-aware grounding",
                "Optimization and Faithfulness (Sec. 7.3)\n• reinforcement learning\n• preference optimization\n• hallucination control",
            ],
        ),
        (
            "Extended Scenarios\n(Sec. 8)",
            [
                "Video Segmentation (Sec. 8.1)\n• tracking-aware grounding\n• video reasoning\n• audio-visual referring",
                "3D/Multiview Grounding (Sec. 8.2)\n• point-cloud masks\n• 3D referring\n• cross-view alignment",
                "Domain-specific Grounding (Sec. 8.3)\n• remote sensing/medicine\n• affordance/embodiment\n• guideline-consistent masks",
            ],
        ),
    ]

    root_bottom = root_y
    bus_y = 6.93
    connector(ax, root_x + root_w / 2, root_bottom, root_x + root_w / 2, bus_y, arrow=False)
    ax.plot([col_x[0] + col_w / 2, col_x[-1] + col_w / 2], [bus_y, bus_y], color="black", lw=1.1)

    for x, (title, items) in zip(col_x, columns):
        connector(ax, x + col_w / 2, bus_y, x + col_w / 2, top_y + top_h, arrow=True)
        rounded_box(ax, x, top_y, col_w, top_h, title, COLORS["blue_light"], fontsize=6.2)
        stem_x = x + 0.18
        ax.plot([stem_x, stem_x], [top_y, 1.42], color="black", lw=1.1)
        y = 4.30
        for i, item in enumerate(items):
            h = 1.18
            rounded_box(
                ax,
                x + 0.38,
                y,
                col_w - 0.28,
                h,
                item,
                COLORS["box_green"],
                fontsize=4.85,
                lw=1.05,
                italic_lines={1, 2, 3},
                ha="left",
            )
            connector(ax, stem_x, y + h / 2, x + 0.38, y + h / 2, arrow=True)
            y -= 1.65

    save_figure(fig, Path(out_dir) / "background_taxonomy")


def main():
    root = Path(__file__).resolve().parents[2]
    out_dir = root / "Fig"
    make_fig3(out_dir)
    make_fig4(out_dir)
    print(f"Saved redrawn figures to {out_dir}")


if __name__ == "__main__":
    main()
