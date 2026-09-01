from __future__ import annotations

import csv
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle

ROOT = Path(__file__).resolve().parents[1]
FIG = ROOT / "figures"
TAB = ROOT / "tables"
FIG.mkdir(exist_ok=True)
TAB.mkdir(exist_ok=True)

TEAL = "#0A7770"
TEAL_DARK = "#075B56"
TEAL_LIGHT = "#DDEFEA"
BLUE = "#32678E"
ORANGE = "#B7661B"
RED = "#A33A32"
GRAY = "#666666"
LIGHT_GRAY = "#E8E8E8"
DARK = "#222222"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.titlesize": 11,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "figure.dpi": 150,
    "savefig.dpi": 300,
    "axes.spines.top": False,
    "axes.spines.right": False,
})

families = ["Ministral 3 8B", "OLMo 3 7B", "Qwen3 8B"]
family_ids = ["ministral-3-8b", "olmo-3-7b", "qwen3-8b"]
judges = ["Judge A (Sonnet 5)", "Judge B (GPT-5)"]

uar = {
    "ministral-3-8b": {
        "Judge A": (64.3, 49.8, 14.5),
        "Judge B": (61.2, 43.7, 17.6),
        "spread": 3.1,
    },
    "olmo-3-7b": {
        "Judge A": (75.5, 61.6, 13.9),
        "Judge B": (74.5, 54.1, 20.4),
        "spread": 6.5,
    },
    "qwen3-8b": {
        "Judge A": (60.2, 49.8, 10.4),
        "Judge B": (53.1, 43.3, 9.8),
        "spread": 0.6,
    },
}

adjusted = {
    "ministral-3-8b": {
        "raw_uar_improvement_pp": 17.6,
        "adjusted_uar_improvement_pp": 14.2,
        "uar_from_refusal_pp": 3.4,
        "uar_gain_survives_pct": 81,
        "raw_acc_change_pp": -49.7,
        "adjusted_acc_change_pp": -41.8,
        "acc_from_refusal_pp": -7.9,
    },
    "olmo-3-7b": {
        "raw_uar_improvement_pp": 20.4,
        "adjusted_uar_improvement_pp": 17.7,
        "uar_from_refusal_pp": 2.7,
        "uar_gain_survives_pct": 87,
        "raw_acc_change_pp": -25.3,
        "adjusted_acc_change_pp": -11.8,
        "acc_from_refusal_pp": -13.4,
    },
    "qwen3-8b": {
        "raw_uar_improvement_pp": 9.8,
        "adjusted_uar_improvement_pp": 6.5,
        "uar_from_refusal_pp": 3.3,
        "uar_gain_survives_pct": 66,
        "raw_acc_change_pp": -26.9,
        "adjusted_acc_change_pp": -19.7,
        "acc_from_refusal_pp": -7.2,
    },
}
for row in adjusted.values():
    row["acc_loss_per_adjusted_uar_gain"] = abs(row["adjusted_acc_change_pp"]) / row["adjusted_uar_improvement_pp"]
    row["adjusted_uar_gain_per_acc_loss"] = row["adjusted_uar_improvement_pp"] / abs(row["adjusted_acc_change_pp"])

# -------------------- Tables --------------------
with (TAB / "model_panel.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["family", "base_model", "revision", "condition_0", "condition_2", "condition_3", "trained_seeds"])
    w.writerow(["qwen3-8b", "Qwen/Qwen3-8B", "b968826d9c46dd6066d109eabc6255188de91218", "untouched instruction checkpoint", "character SFT", "character SFT+DPO", "11;23;42;67;101"])
    w.writerow(["ministral-3-8b", "mistralai/Ministral-3-8B-Instruct-2512-BF16", "f6fae9795746f63c9be8344932f01275f3c63734", "untouched instruction checkpoint", "character SFT", "character SFT+DPO", "11;23;42;67;101"])
    w.writerow(["olmo-3-7b", "allenai/Olmo-3-7B-Instruct", "6e5971d9eba42665f5bd5a0fcf047f299ce1dccc", "untouched instruction checkpoint", "character SFT", "character SFT+DPO", "11;23;42;67;101"])

with (TAB / "per_family_per_judge_uar.csv").open("w", newline="", encoding="utf-8") as f:
    fields = ["family", "judge", "baseline_uar_pct", "c3_uar_pct", "uar_improvement_pp", "judge_spread_pp", "family_verdict"]
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for fid in family_ids:
        for judge in ["Judge A", "Judge B"]:
            b, c, imp = uar[fid][judge]
            w.writerow({
                "family": fid,
                "judge": judge,
                "baseline_uar_pct": b,
                "c3_uar_pct": c,
                "uar_improvement_pp": imp,
                "judge_spread_pp": uar[fid]["spread"],
                "family_verdict": "DOES_NOT_MEET",
            })

with (TAB / "refusal_adjusted_judge_b.csv").open("w", newline="", encoding="utf-8") as f:
    fields = [
        "family", "raw_uar_improvement_pp", "adjusted_uar_improvement_pp", "uar_from_refusal_pp",
        "uar_gain_survives_pct", "raw_acc_change_pp", "adjusted_acc_change_pp", "acc_from_refusal_pp",
        "acc_loss_per_adjusted_uar_gain", "adjusted_uar_gain_per_acc_loss",
    ]
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    for fid in family_ids:
        row = {"family": fid, **adjusted[fid]}
        row["acc_loss_per_adjusted_uar_gain"] = round(row["acc_loss_per_adjusted_uar_gain"], 3)
        row["adjusted_uar_gain_per_acc_loss"] = round(row["adjusted_uar_gain_per_acc_loss"], 3)
        w.writerow({k: row[k] for k in fields})

with (TAB / "g1_reliability_runs.csv").open("w", newline="", encoding="utf-8") as f:
    fields = ["run", "status", "outcome", "effective_n", "ac1", "ci_low", "ci_high", "raw_agreement", "incomplete_count"]
    w = csv.DictWriter(f, fieldnames=fields)
    w.writeheader()
    rows = [
        {"run":"run_1", "status":"VOID - provenance inadequate", "outcome":"UAR", "effective_n":119, "ac1":0.854, "ci_low":0.763, "ci_high":0.928, "raw_agreement":"not used for canonical result", "incomplete_count":1},
        {"run":"run_1", "status":"VOID - provenance inadequate", "outcome":"ACC", "effective_n":120, "ac1":0.859, "ci_low":0.768, "ci_high":0.938, "raw_agreement":"not used for canonical result", "incomplete_count":0},
        {"run":"run_2", "status":"CANONICAL - provenance complete", "outcome":"UAR", "effective_n":119, "ac1":0.911, "ci_low":0.840, "ci_high":0.967, "raw_agreement":0.933, "incomplete_count":0},
        {"run":"run_2", "status":"CANONICAL - provenance complete", "outcome":"ACC", "effective_n":120, "ac1":0.826, "ci_low":0.724, "ci_high":0.920, "raw_agreement":0.908, "incomplete_count":0},
    ]
    w.writerows(rows)

with (TAB / "provenance_summary.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["field", "value", "qualification"])
    rows = [
        ("plan", "pl_a76997a37c338a45", "19/19 nodes succeeded; no evictions"),
        ("compute", "39.77 GPU-h", "of 248 GPU-h authorized for the completed bank"),
        ("matrix", "3 families x 5 seeds", "15 C2 SFT + 15 C3 DPO + 3 C0 baseline artifacts"),
        ("sealed_artifacts", "33", "33 distinct ciphertext digests; seal integrity verified"),
        ("code_bundle_sha256", "e0bf9a948a623b6eb464fc17cec8ba7f96377a69c663ab68edb29af2be437b71", "identical across all 33 artifacts"),
        ("validation_sha256", "eaaadaeb589e4b1236d18636289595a0a70b08daeb142f070af5c67104400fa5", "200-prompt validation split"),
        ("readout_rows", "3546", "197 scorable items x 18 C0/C3 artifacts"),
        ("execution_git_commit", "unknown", "all 33 manifests; do not replace with publication commit"),
        ("claim_tier", "INTERNAL REVIEW ONLY", "no external audit; primary-test holdout untouched"),
    ]
    w.writerows(rows)

with (TAB / "claim_evidence_matrix.csv").open("w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["claim_id", "claim", "status", "evidence", "public_wording"])
    w.writerow(["TR2-C1", "The frozen intervention reduced UAR on the validation split in all three families under both judges.", "SUPPORTED - DEVELOPMENT TIER", "Per-family per-judge C0-to-C3 rates", "Reduced unsupported assertions on this validation benchmark."])
    w.writerow(["TR2-C2", "The complete utility-preservation bar was met.", "NOT SUPPORTED", "ACC criterion failed in every family under both judges; coverage failed under Judge B", "No family met the pre-registered development-tier utility-preservation bar."])
    w.writerow(["TR2-C3", "The UAR change was only generic refusal.", "NOT SUPPORTED BY JUDGE-B ADJUSTMENT", "66-87% of UAR gain remained after dropping generic-refusal items", "Most of the Judge-B-measured UAR gain survived the generic-refusal adjustment."])
    w.writerow(["TR2-C4", "The intervention improved truthfulness or factual knowledge.", "NOT ESTABLISHED", "ACC losses; capability not evaluated; bespoke validation benchmark", "Do not use this claim."])
    w.writerow(["TR2-C5", "OLMo was the best successor target among the tested configurations.", "SUPPORTED AS A PIVOT DECISION, NOT A MODEL PASS", "Best adjusted UAR/ACC exchange rate", "OLMo had the least damaging measured frontier and merits optimization."])
    w.writerow(["TR2-C6", "The result is independently or externally validated.", "FALSE", "No external audit occurred", "Internal review only."])

summary = {
    "report_version": "1.0",
    "date": "2026-09-01",
    "tier": "development",
    "claim_tier": "internal-review-only",
    "primary_holdout": "untouched",
    "model_release_eligible": False,
    "families": family_ids,
    "seeds": [11, 23, 42, 67, 101],
    "plan_id": "pl_a76997a37c338a45",
    "gpu_hours": 39.77,
    "canonical_g1": {
        "uar": {"n":119, "ac1":0.911, "ci95":[0.840,0.967], "raw_agreement":0.933},
        "acc": {"n":120, "ac1":0.826, "ci95":[0.724,0.920], "raw_agreement":0.908},
    },
    "result": "No family met the pre-registered validation-tier utility-preservation bar under either judge.",
}
(TAB / "research_record.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

# -------------------- Figure 1: design --------------------
fig, ax = plt.subplots(figsize=(10.5, 4.9))
ax.set_xlim(0, 10.5)
ax.set_ylim(0, 5.1)
ax.axis("off")

def box(x, y, w, h, text, fc="white", ec=TEAL, lw=1.5, fs=9, weight="normal"):
    patch = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=0.08", fc=fc, ec=ec, lw=lw)
    ax.add_patch(patch)
    ax.text(x+w/2, y+h/2, text, ha="center", va="center", fontsize=fs, weight=weight, color=DARK)
    return patch

def arrow(x1,y1,x2,y2, color=GRAY):
    ax.add_patch(FancyArrowPatch((x1,y1),(x2,y2),arrowstyle="-|>",mutation_scale=12,lw=1.2,color=color))

ax.text(0.1, 4.82, "Frozen multi-family design", fontsize=14, weight="bold", color=TEAL_DARK)
ax.text(0.1, 4.52, "One ordered character SFT -> DPO recipe; five paired seeds per family; validation split only", fontsize=9.5, color=GRAY)

ys = [3.55, 2.45, 1.35]
for y, fam in zip(ys, families):
    box(0.25,y,1.65,0.62,fam,fc=TEAL_LIGHT,weight="bold")
    box(2.35,y,1.55,0.62,"C0\nuntouched base",fc="white",ec=BLUE)
    box(4.40,y,1.55,0.62,"C2\ncharacter SFT",fc="white",ec=TEAL)
    box(6.45,y,1.55,0.62,"C3\nSFT + DPO",fc="white",ec=TEAL_DARK)
    box(8.55,y,1.55,0.62,"200-prompt\nvalidation readout",fc="#F7F7F7",ec=GRAY)
    arrow(1.9,y+0.31,2.35,y+0.31)
    arrow(3.90,y+0.31,4.40,y+0.31)
    arrow(5.95,y+0.31,6.45,y+0.31)
    arrow(8.00,y+0.31,8.55,y+0.31)
    ax.text(5.18,y-0.18,"seeds 11, 23, 42, 67, 101",ha="center",va="top",fontsize=7.5,color=GRAY)

box(2.8,0.2,4.9,0.62,"Primary-test holdout: untouched and not consumed by this release",fc="#FFF4E6",ec=ORANGE,weight="bold")
ax.text(10.25,0.13,"Development-tier evidence",ha="right",va="bottom",fontsize=8,color=GRAY)
fig.tight_layout()
for ext in ("png","pdf","svg"):
    fig.savefig(FIG / f"figure1_experimental_design.{ext}", bbox_inches="tight")
plt.close(fig)

# -------------------- Figure 2: UAR dumbbells --------------------
rows = []
for fam, fid in zip(families, family_ids):
    for judge in ["Judge A", "Judge B"]:
        b,c,imp = uar[fid][judge]
        rows.append((fam,judge,b,c,imp))
fig, ax = plt.subplots(figsize=(9.6, 5.2))
ypos = np.arange(len(rows))[::-1]
for y,(fam,judge,b,c,imp) in zip(ypos, rows):
    ax.plot([c,b],[y,y], color="#B8B8B8", lw=2, zorder=1)
    ax.scatter(b,y,s=55,color=GRAY,zorder=3,label="C0 baseline" if y==ypos[0] else None)
    ax.scatter(c,y,s=62,color=TEAL,zorder=3,label="C3 SFT+DPO" if y==ypos[0] else None)
    ax.text(c-1.0,y+0.19,f"-{imp:.1f} pp",ha="right",va="bottom",fontsize=7.8,color=TEAL_DARK,weight="bold")
ax.set_yticks(ypos)
ax.set_yticklabels([f"{fam} - {judge}" for fam,judge,_,_,_ in rows])
ax.set_xlim(38,80)
ax.set_xlabel("Unsupported assertion rate (%) - lower is better")
fig.suptitle("C3 reduced unsupported assertions under both judges in every family", x=0.10, y=0.99, ha="left", weight="bold", color=TEAL_DARK, fontsize=11)
ax.set_title("C0 baseline to final SFT+DPO condition on the 200-prompt validation split", loc="left", fontsize=8.5, color=GRAY, pad=10)
ax.grid(axis="x", color=LIGHT_GRAY, lw=0.8)
ax.legend(frameon=False,loc="lower right")
fig.tight_layout(rect=[0,0,1,0.92])
for ext in ("png","pdf","svg"):
    fig.savefig(FIG / f"figure2_uar_by_family_and_judge.{ext}", bbox_inches="tight")
plt.close(fig)

# -------------------- Figure 3: adjusted frontier --------------------
fig, ax = plt.subplots(figsize=(7.6, 5.4))
# Success region: at least 5pp UAR and <=3pp ACC loss
ax.add_patch(Rectangle((5,0),17,3,facecolor=TEAL_LIGHT,edgecolor="none",alpha=0.9,zorder=0))
ax.text(21.6,1.5,"pre-registered\nsuccess region",ha="right",va="center",fontsize=8,color=TEAL_DARK,weight="bold")
markers = {"ministral-3-8b":"o","olmo-3-7b":"s","qwen3-8b":"^"}
labels = {"ministral-3-8b":"Ministral 3 8B","olmo-3-7b":"OLMo 3 7B","qwen3-8b":"Qwen3 8B"}
for fid in family_ids:
    x = adjusted[fid]["adjusted_uar_improvement_pp"]
    y = abs(adjusted[fid]["adjusted_acc_change_pp"])
    col = TEAL if fid == "olmo-3-7b" else BLUE if fid == "ministral-3-8b" else ORANGE
    ax.scatter(x,y,s=105,marker=markers[fid],color=col,zorder=3)
    dy = -2.6 if fid == "ministral-3-8b" else 1.2
    ax.annotate(f"{labels[fid]}\n{x:.1f} pp UAR gain, {y:.1f} pp ACC loss",
                (x,y),xytext=(7,dy),textcoords="offset points",fontsize=8.2,color=DARK)
ax.axvline(5,color="#AAAAAA",lw=1,ls="--")
ax.axhline(3,color="#AAAAAA",lw=1,ls="--")
ax.set_xlim(0,22)
ax.set_ylim(0,46)
ax.set_xlabel("Refusal-adjusted UAR improvement (percentage points) - more is better")
ax.set_ylabel("Refusal-adjusted ACC loss (percentage points) - less is better")
fig.suptitle("The intervention moved the frontier, but no family preserved grounded answering", x=0.10, y=0.99, ha="left", weight="bold", color=TEAL_DARK, fontsize=11)
ax.set_title("Judge B only; generic-refusal items removed from both paired arms", loc="left", fontsize=8.5, color=GRAY, pad=10)
ax.grid(color=LIGHT_GRAY,lw=0.8)
fig.tight_layout(rect=[0,0,1,0.92])
for ext in ("png","pdf","svg"):
    fig.savefig(FIG / f"figure3_refusal_adjusted_frontier.{ext}", bbox_inches="tight")
plt.close(fig)

# -------------------- Figure 4: judge repeatability --------------------
fig, ax = plt.subplots(figsize=(7.8, 4.8))
labels_x = ["UAR - void run", "UAR - canonical", "ACC - void run", "ACC - canonical"]
vals = np.array([0.854,0.911,0.859,0.826])
lo = np.array([0.763,0.840,0.768,0.724])
hi = np.array([0.928,0.967,0.938,0.920])
colors = ["#AAAAAA", TEAL, "#AAAAAA", TEAL]
x = np.arange(4)
for xi,v,l,h,c in zip(x,vals,lo,hi,colors):
    ax.errorbar([xi], [v], yerr=[[v-l],[h-v]], fmt="none", ecolor=c, capsize=4, lw=1.8)
    ax.scatter(xi,v,s=75,color=c,zorder=3)
    ax.text(xi,v+0.023,f"{v:.3f}",ha="center",va="bottom",fontsize=8,weight="bold",color=DARK)
ax.axhline(0.80,color=ORANGE,ls="--",lw=1.1,label="AC1 point threshold 0.80")
ax.axhline(0.67,color="#999999",ls=":",lw=1.1,label="CI-lower threshold 0.67")
ax.set_xticks(x)
ax.set_xticklabels(labels_x)
ax.set_ylim(0.62,1.0)
ax.set_ylabel("Gwet's AC1 with 95% cluster-bootstrap interval")
fig.suptitle("One judging procedure produced materially different reliability estimates", x=0.10, y=0.99, ha="left", weight="bold", color=TEAL_DARK, fontsize=11)
ax.set_title("The first run is retained as void for provenance; the second is the canonical gate result", loc="left", fontsize=8.5, color=GRAY, pad=10)
ax.grid(axis="y",color=LIGHT_GRAY,lw=0.8)
ax.legend(frameon=False,loc="lower right",fontsize=8)
fig.tight_layout(rect=[0,0,1,0.92])
for ext in ("png","pdf","svg"):
    fig.savefig(FIG / f"figure4_g1_judge_repeatability.{ext}", bbox_inches="tight")
plt.close(fig)

# -------------------- Figure 5: result summary --------------------
fig, ax = plt.subplots(figsize=(9.5, 3.5))
ax.axis("off")
ax.text(0.0,0.93,"What the development-tier bank established",fontsize=13,weight="bold",color=TEAL_DARK,transform=ax.transAxes)
items = [
    ("UAR direction", "Improved in all 3 families\nunder both judges", TEAL_LIGHT, TEAL_DARK),
    ("Utility bar", "0 of 3 families met\nthe complete bar", "#FBE7E5", RED),
    ("Primary holdout", "Untouched", "#FFF4E6", ORANGE),
    ("Model release", "No checkpoint\nrecommended", "#F1F1F1", DARK),
]
for i,(head,body,fc,ec) in enumerate(items):
    x0 = 0.01 + i*0.247
    rect = FancyBboxPatch((x0,0.16),0.225,0.56,boxstyle="round,pad=0.012,rounding_size=0.025",fc=fc,ec=ec,lw=1.2,transform=ax.transAxes)
    ax.add_patch(rect)
    ax.text(x0+0.1125,0.57,head,ha="center",va="center",fontsize=9,weight="bold",color=ec,transform=ax.transAxes)
    ax.text(x0+0.1125,0.35,body,ha="center",va="center",fontsize=8.0,color=DARK,linespacing=1.25,transform=ax.transAxes)
ax.text(0.0,0.03,"Claim tier: internal review only. Capability preservation was not evaluated. No external audit was performed.",fontsize=8.2,color=GRAY,transform=ax.transAxes)
fig.tight_layout()
for ext in ("png","pdf","svg"):
    fig.savefig(FIG / f"figure5_result_summary.{ext}", bbox_inches="tight")
plt.close(fig)

print(f"Wrote figures to {FIG}")
print(f"Wrote tables to {TAB}")
