#!/usr/bin/env python3
"""Rebuild the six public scientific figures from the frozen aggregate values.

This script intentionally uses no private task content, raw completions, or external assets.
"""
from pathlib import Path
import json, math
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"figures"
OUT.mkdir(exist_ok=True)

def save(fig,stem):
    for ext in ("png","svg","pdf"):
        kw={"bbox_inches":"tight"}
        if ext=="png": kw["dpi"]=240
        fig.savefig(OUT/f"{stem}.{ext}",**kw)
    plt.close(fig)

fig=plt.figure(figsize=(10.5,7.2)); ax=plt.axes(); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
steps=[("P-BREVE-01","first-pass no-go preserved"),("P-BREVE-01-R2","micro-SFT + conservative DPO"),("One-epoch result","efficiency target missed at both-seed bar"),("Two-epoch screen","apparent dose response on code tasks"),("Serving control","untrained base reproduced termination shift"),("Original evaluator","24/24 shortcut programs passed"),("Replacement evaluator","improved, but independent qualification failed"),("Final disposition","no model, bank, or release candidate")]
y=np.linspace(.91,.12,len(steps))
for i,((h,s),yy) in enumerate(zip(steps,y),1):
    ax.add_patch(FancyBboxPatch((.12,yy-.043),.76,.078,boxstyle="round,pad=0.012",fill=False,linewidth=1.4)); ax.text(.15,yy+.008,f"{i}. {h}",fontsize=12.5,weight="bold",va="center"); ax.text(.15,yy-.021,s,fontsize=10.2,va="center")
    if i<len(steps): ax.add_patch(FancyArrowPatch((.5,yy-.047),(.5,y[i]+.045),arrowstyle="-|>",mutation_scale=14))
ax.text(.5,.985,"P-BREVE-01-R2 study lineage and claim disposition",ha="center",va="top",fontsize=17,weight="bold"); ax.text(.5,.035,"P-BREVE-02 remains reserved for a future locked-recipe Western-base replication.",ha="center",fontsize=9.5); save(fig,"figure1_study_lineage")

fig=plt.figure(figsize=(9.6,5.8)); ax=plt.axes(); labels=["SFT-only","SFT + DPO\n(one epoch)","DPO marginal\nover SFT"]; a=[-10.3,-10.9,-.6]; b=[4.3,4.9,.6]; x=np.arange(3); w=.34
b1=ax.bar(x-w/2,a,w,label="seed 1729"); b2=ax.bar(x+w/2,b,w,label="seed 2718"); ax.axhline(20,linestyle="--",linewidth=1.2,label="required reduction (+20%)"); ax.axhline(0,linewidth=.8); ax.set_xticks(x,labels); ax.set_ylabel("Reasoning reduction versus base (%)"); ax.set_title("The configured one-epoch recipe did not meet the two-seed efficiency target"); ax.legend(frameon=False,ncol=3,loc="upper center"); ax.grid(axis="y",alpha=.25)
for bars in (b1,b2):
    for bar in bars:
        v=bar.get_height(); ax.text(bar.get_x()+bar.get_width()/2,v+(.8 if v>=0 else -1.4),f"{v:+.1f}%",ha="center",va="bottom" if v>=0 else "top",fontsize=9)
ax.text(.01,.02,"Sign convention: positive = fewer tokens; negative = more tokens.",transform=ax.transAxes,fontsize=9); save(fig,"figure2_one_epoch_reduction")

fig=plt.figure(figsize=(9.4,5.8)); ax=plt.axes(); xx=np.arange(2); ax.plot(xx,[6407,608],marker="o",linewidth=2,label="restricted mean reasoning length"); ax.plot(xx,[21401,944],marker="s",linewidth=2,label="tokens per strict success"); ax.set_yscale("log"); ax.set_xticks(xx,["base @ xhigh","base @ medium"]); ax.set_ylabel("Tokens (log scale)"); ax.set_title("Serving-time effort control reproduced the code-stratum termination shift"); ax.legend(frameon=False); ax.grid(axis="y",alpha=.25); ax.annotate("cap exhaustion: 65%",(0,6407),xytext=(-.02,9000),ha="center",arrowprops={"arrowstyle":"->"}); ax.annotate("cap exhaustion: 0/20\n(95% upper bound 16.8%)",(1,608),xytext=(1,2600),ha="center",arrowprops={"arrowstyle":"->"}); ax.text(.01,.02,"Screened shard; matched-effort correctness comparison remained underpowered.",transform=ax.transAxes,fontsize=9); save(fig,"figure3_serving_effort_control")

fig=plt.figure(figsize=(10,6)); ax=plt.axes(); labels=["Original bank:\nbroad shortcuts","Replacement runtime:\nbroad shortcuts","Replacement certification:\nbroad shortcuts","Replacement certification:\nnear-miss / partial","Blind mutation population:\nprovably wrong mutants"]; rates=[100,154/322*100,0,7/157*100,52/1862*100]; nums=["24/24","154/322","0/322","7/157","52/1,862"]; bars=ax.barh(np.arange(5),rates); ax.set_yticks(np.arange(5),labels); ax.invert_yaxis(); ax.set_xlabel("False-accept rate within the stated probe population (%)"); ax.set_title("Executable evaluation improved, but independent qualification still failed"); ax.grid(axis="x",alpha=.25)
for bar,num,rate in zip(bars,nums,rates): ax.text(min(rate+1,93),bar.get_y()+bar.get_height()/2,f"{num}  ({rate:.2f}%)",va="center",fontsize=9.5)
save(fig,"figure4_evaluator_qualification")

fig=plt.figure(figsize=(9.8,5.8)); ax=plt.axes(); labels=["AST population:\nat least one leak","AST population:\nno detected leak","Cross-method union:\nknown certification flaw"]; vals=[19,21,21]; bars=ax.bar(np.arange(3),vals); ax.set_ylim(0,40); ax.set_xticks(np.arange(3),labels); ax.set_ylabel("Tasks out of 40"); ax.set_title("Two different 21-of-40 quantities must not be conflated"); ax.grid(axis="y",alpha=.25)
for i,(bar,v) in enumerate(zip(bars,vals)): ax.text(bar.get_x()+bar.get_width()/2,v+.8,("at least " if i==2 else "")+f"{v}/40",ha="center",fontsize=10.5,weight="bold")
ax.text(.5,-.22,"Cross-method lower bound = 7 previously identified tasks + 14 newly adjudicated tasks outside that set.\nThe AST-only no-leak count is the complement 40 − 19 and has opposite polarity.",transform=ax.transAxes,ha="center",fontsize=9.2); save(fig,"figure5_task_count_disambiguation")

fig=plt.figure(figsize=(10.5,7)); ax=plt.axes(); ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off"); checks=[("1","Identity and independence","Exact artifact, model, task-family, and statistical unit"),("2","Contract clarity","Prompt, tests, and reference agree on every scored behaviour"),("3","Channel separation","Visible runtime checks cannot become the hidden score"),("4","Bidirectional discrimination","Wrong programs fail; valid alternatives pass"),("5","Estimand integrity","Censoring, denominators, retention, and units are explicit"),("6","Production-path binding","The executed authority is the authority named in provenance"),("7","Power and requalification","Simulate the exact rule; use an independent post-repair population")]; ys=np.linspace(.87,.13,7)
for (n,h,s),yy in zip(checks,ys): ax.add_patch(FancyBboxPatch((.08,yy-.048),.84,.082,boxstyle="round,pad=0.01",fill=False,linewidth=1.2)); ax.text(.105,yy,n,fontsize=13,weight="bold",va="center"); ax.text(.16,yy+.012,h,fontsize=11.8,weight="bold",va="center"); ax.text(.16,yy-.020,s,fontsize=9.6,va="center")
ax.text(.5,.975,"Vinci Eval Integrity 0.1",ha="center",va="top",fontsize=18,weight="bold"); ax.text(.5,.035,"Any failed or unverified check blocks qualified-evaluator language for model selection, optimization, release, or product claims.",ha="center",fontsize=9.3); save(fig,"figure6_vinci_eval_integrity")
