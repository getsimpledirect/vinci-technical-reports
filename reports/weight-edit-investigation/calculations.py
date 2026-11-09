#!/usr/bin/env python3
"""Validate and recalculate this aggregate-only directory with the standard library."""
import argparse
import copy
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PIN = '4d09ba6d6a7e891dd8063974dfe81b3d78e3494f'
PUBLIC_ROOT = 'https://github.com/RikiyaT/lm_understand-logs/blob/' + PIN + '/'
PUBLIC_URLS = {
 'https://rikiyat.github.io/blog/weight-space-programming/',
 *(PUBLIC_ROOT + p for p in [
  'exp8_math/README.md','exp8_math/eval/unedited/merged.json',
  'exp8_math/eval/p50c/merged.json','exp8_math/runs/p50c/edit/manifest.json',
  'exp8_math/gemma_followup/README.md'])}
PAIR_KEYS = {'id','model','dataset','stage','reference_arm','comparison_arm','n',
 'reference_correct','comparison_correct','counts','reported_difference_pp',
 'reported_95_percent_ci_pp','reported_interval_method','reported_resamples',
 'selected_after_observed_outcomes','count_provenance','evidence_basis',
 'configured_max_new_tokens','thinking_mode','evaluated_artifact_identity_verified','evidence_excerpt_ids'}
DIAG_KEYS = {'comparison_id','arm','n','cap_hit','mean_tokens','median_tokens',
 'no_boxed','unparseable','continued_rows','configured_max_new_tokens',
 'evaluated_artifact_identity_verified','evidence_basis','evidence_excerpt_ids','normalization_note'}
PUBLIC_KEYS = {'id','model','run','forward_call_budget','benchmark','accuracy_percent',
 'samples_per_problem','aggregation','citations'}
CELL_KEYS = {'both_correct','reference_only_correct','comparison_only_correct','both_wrong'}

class Invalid(ValueError):
    def __init__(self, code, detail):
        self.code = code
        super().__init__(code + ': ' + detail)

def need(condition, code, detail):
    if not condition:
        raise Invalid(code, detail)

def integer(value):
    return isinstance(value,int) and not isinstance(value,bool)

def number(value):
    return isinstance(value,(int,float)) and not isinstance(value,bool) and math.isfinite(value)

def load():
    return {key: json.loads((ROOT/'data'/filename).read_text()) for key,filename in [
      ('pairs','local-paired-aggregates.json'),('diagnostics','completion-diagnostics.json'),
      ('public','public-author-aggregates.json'),('sources','public-sources.json'),
      ('context','context-and-limits.json'),('excerpts','source-excerpts.json')]}

def validate(payload):
    pairs, diagnostics = payload['pairs']['comparisons'],payload['diagnostics']['rows']
    public, sources = payload['public']['rows'],payload['sources']['sources']
    need(len(pairs)==16 and len(diagnostics)==14 and len(public)==37,'row-coverage','Expected 16 paired,14 diagnostic,37 public rows.')
    need(len({r['id'] for r in pairs})==16,'row-coverage','Paired IDs must be unique.')
    source_ids = {s['id'] for s in sources}
    need(len(source_ids)==6 and {s['url'] for s in sources}==PUBLIC_URLS,'public-source','Only the six explicitly listed public citations are permitted.')
    excerpt_ids={r['id'] for r in payload['excerpts']['excerpts']}
    need(len(excerpt_ids)==7,'excerpt-coverage','Seven sanitized aggregate excerpts.')
    pair_map = {r['id']:r for r in pairs}
    for r in pairs:
        label = r['id']
        need(all(e in excerpt_ids for e in r['evidence_excerpt_ids']),'excerpt-join',label)
        need(set(r)==PAIR_KEYS and set(r['counts'])==CELL_KEYS,'schema',label)
        n,a,b = r['n'],r['reference_correct'],r['comparison_correct']
        cells = r['counts']; values = list(cells.values())
        need(integer(n) and n>0 and all(integer(v) and 0<=v<=n for v in [a,b,*values]),'count-bound',label)
        need(sum(values)==n,'paired-total',label)
        need(cells['both_correct']+cells['reference_only_correct']==a and cells['both_correct']+cells['comparison_only_correct']==b,'paired-margin',label)
        need(number(r['reported_difference_pp']) and abs(100*(b-a)/n-r['reported_difference_pp'])<=0.0050001,'difference',label)
        interval = r['reported_95_percent_ci_pp']
        need(len(interval)==2 and all(number(v) for v in interval) and -100<=interval[0]<=interval[1]<=100,'interval',label)
        need(r['reported_interval_method']=='reported paired percentile bootstrap' and r['reported_resamples']==10000,'interval-method',label)
        need(r['configured_max_new_tokens'] is None and r['thinking_mode'] is None,'unknown-setting',label)
        need(r['evaluated_artifact_identity_verified'] is False,'unknown-identity',label)
        need(r['evidence_basis'] in {'partial_private_reader_excerpt','secondary_private_audit_summary'},'provenance',label)
    for r in diagnostics:
        need(set(r)==DIAG_KEYS,'schema','Diagnostic fields.')
        need(r['comparison_id'] in pair_map and r['n']==pair_map[r['comparison_id']]['n'],'diagnostic-join',r['comparison_id'])
        n = r['n']
        need(all(e in excerpt_ids for e in r['evidence_excerpt_ids']),'excerpt-join',r['comparison_id'])
        for key in ['cap_hit','no_boxed','unparseable','continued_rows']:
            v=r[key];need(v is None or (integer(v) and 0<=v<=n),'cap-bound',r['comparison_id']+'/'+key)
        for key in ['mean_tokens','median_tokens']:
            v=r[key];need(v is None or (number(v) and v>=0),'token-bound',r['comparison_id']+'/'+key)
        need(r['configured_max_new_tokens'] is None,'unknown-setting',r['comparison_id'])
        need(r['evaluated_artifact_identity_verified'] is False,'unknown-identity',r['comparison_id'])
    need(len({r['id'] for r in public})==37,'row-coverage','Public IDs must be unique.')
    for r in public:
        need(set(r)==PUBLIC_KEYS,'schema','Public aggregate fields.')
        need(number(r['accuracy_percent']) and 0<=r['accuracy_percent']<=100,'public-rate',r['id'])
        need(integer(r['samples_per_problem']) and r['samples_per_problem']>0,'public-sampling',r['id'])
        need(integer(r['forward_call_budget']) and r['forward_call_budget']>=0,'public-budget',r['id'])
        need(r['citations'] and all(c['source_id'] in source_ids for c in r['citations']),'public-source',r['id'])
    pending = payload['context']['piccolo_500_item_test']
    need(pending['n_reported']==500 and pending['base_correct'] is None and pending['edited_correct'] is None and pending['random_correct'] is None and pending['reported_difference_pp'] is None and pending['reported_95_percent_ci_pp'] is None,'unknown-result','500-item result must remain unknown.')
    need(pending['decision_rule_timing_verified'] is False and pending['evaluated_artifact_identity_verified'] is False,'unknown-identity','500-item scope.')

def calculate(r):
    n=r['n']; counts=r['counts']
    minus,plus=counts['reference_only_correct'],counts['comparison_only_correct']
    pminus,pplus=minus/n,plus/n; pzero=1-pminus-pplus
    distribution=[1.0]
    for _ in range(n):
        nxt=[0.0]*(len(distribution)+2)
        for j,value in enumerate(distribution):
            nxt[j]+=value*pminus
            nxt[j+1]+=value*pzero
            nxt[j+2]+=value*pplus
        distribution=nxt
    need(abs(math.fsum(distribution)-1)<1e-10,'distribution-mass',r['id'])
    endpoints=[]; cumulative=0.0; target=0
    for j,probability in enumerate(distribution):
        cumulative+=probability
        while target<2 and cumulative>=[0.025,0.975][target]:
            endpoints.append(100*(j-n)/n);target+=1
    discordant=minus+plus
    pvalue=1.0 if discordant==0 else min(1.0,2*sum(math.comb(discordant,k) for k in range(min(minus,plus)+1))/(2**discordant))
    return {'id':r['id'],'n':n,'reference_accuracy_percent':round(100*r['reference_correct']/n,10),
      'comparison_accuracy_percent':round(100*r['comparison_correct']/n,10),
      'difference_pp':round(100*(plus-minus)/n,10),
      'reported_95_percent_ci_pp':r['reported_95_percent_ci_pp'],
      'recomputed_empirical_bootstrap_95_percentiles_pp':[round(v,10) for v in endpoints],
      'exact_two_sided_mcnemar_p':pvalue,
      'selected_after_observed_outcomes':r['selected_after_observed_outcomes']}

def recompute(pairs):
    return {'method':'Exact enumeration using floating-point arithmetic of the empirical paired bootstrap distribution: n independent draws of delta -1,0,+1 with observed cell probabilities; 2.5th and 97.5th percentiles. No random draws.',
      'limits':'Not an exact-coverage interval; conditional on the chosen edit and sample. Does not account for edit selection, adaptive looks, contamination or multiple comparisons. Reported finite-draw intervals remain separate.',
      'mcnemar_method':'Exact two-sided Binomial(discordant,0.5) tail doubled and capped at one. Secondary paired diagnostic, not adjusted for multiple comparisons.',
      'rows':[calculate(r) for r in pairs]}

def self_test(payload):
    validate(payload)  # Positive control: the shipped complete data must pass.
    controls=[]
    def reject(name, expected, mutate):
        changed=copy.deepcopy(payload);mutate(changed)
        try:
            validate(changed)
        except Invalid as error:
            need(error.code==expected,'control-cause',name+' failed for '+error.code)
            controls.append(name)
        else:
            raise Invalid('control-survived',name)
    reject('changed margin','paired-margin',lambda p:p['pairs']['comparisons'][0].__setitem__('comparison_correct',127))
    reject('invented local cap','unknown-setting',lambda p:p['pairs']['comparisons'][0].__setitem__('configured_max_new_tokens',32768))
    reject('invented artifact linkage','unknown-identity',lambda p:p['pairs']['comparisons'][0].__setitem__('evaluated_artifact_identity_verified',True))
    reject('unapproved citation','public-source',lambda p:p['sources']['sources'][0].__setitem__('url','not-a-public-citation'))
    reject('cap count above sample','cap-bound',lambda p:p['diagnostics']['rows'][0].__setitem__('cap_hit',257))
    reject('invented pending result','unknown-result',lambda p:p['context']['piccolo_500_item_test'].__setitem__('base_correct',0))
    stable={'id':'stable-control','n':8,'reference_correct':4,'comparison_correct':4,
      'counts':{'both_correct':4,'reference_only_correct':0,'comparison_only_correct':0,'both_wrong':4},
      'reported_95_percent_ci_pp':[0,0],'selected_after_observed_outcomes':False}
    result=calculate(stable)
    need(result['difference_pp']==0 and result['recomputed_empirical_bootstrap_95_percentiles_pp']==[0,0] and result['exact_two_sided_mcnemar_p']==1,'numeric-control','Identical arms.')
    improved={**stable,'id':'all-improved-control','n':8,'reference_correct':0,'comparison_correct':8,
      'counts':{'both_correct':0,'reference_only_correct':0,'comparison_only_correct':8,'both_wrong':0}}
    result=calculate(improved)
    need(result['difference_pp']==100 and result['recomputed_empirical_bootstrap_95_percentiles_pp']==[100,100] and result['exact_two_sided_mcnemar_p']==2/256,'numeric-control','All improved pairs.')
    return controls+['identical-arm numerical control','all-improved numerical control']

def check_manifest():
    manifest=ROOT/'MANIFEST.sha256';listed={}
    for line in manifest.read_text().splitlines():
        digest,name=line.split('  ',1)
        need(len(digest)==64 and name not in listed and not Path(name).is_absolute() and '..' not in Path(name).parts,'manifest-format',name)
        listed[name]=digest
    actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and p!=manifest}
    need(not any(p.is_symlink() for p in ROOT.rglob('*')),'manifest-symlink','No symbolic links.')
    need(set(listed)==actual,'manifest-coverage','Manifest must cover the whole tree except itself.')
    for name,digest in listed.items():
        need(hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest,'manifest-hash',name)
    return len(actual)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--json',action='store_true',help='Print recomputed statistics; no files are written.')
    parser.add_argument('--check',action='store_true',help='Validate inputs, controls, stored recalculation and whole-tree manifest (default).')
    args=parser.parse_args();payload=load();validate(payload)
    calculated=recompute(payload['pairs']['comparisons'])
    if args.json:
        print(json.dumps(calculated,indent=2,ensure_ascii=False,allow_nan=False));return
    controls=self_test(payload)
    stored=json.loads((ROOT/'data/recomputed-statistics.json').read_text())
    need(calculated==stored,'recalculation','Stored calculation differs; inspect inputs and method.')
    covered=check_manifest()
    print('PASS: 16 paired comparisons,14 completion diagnostics,37 public rows; '+str(len(controls))+' meaningful controls; '+str(covered)+' files match the complete manifest.')

if __name__=='__main__':
    main()
