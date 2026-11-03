"""Two-class response corpus + length matching.

IMPORTANT LIMITATION: these texts are model-authored (by Claude) in the style
of assistant answers. They are NOT sampled from a deployed LLM's output
distribution. Stage 2 swaps in a real generator to test whether that matters.

Class MED = clinical/health answers, Class GEN = everyday general-knowledge
answers. The two classes differ in vocabulary (medical terms are long and
low-frequency) but matched_pairs() equalises token count and character length
so that count/duration/total-bytes carry no class information.
"""

MED = [
    "Hypertension usually develops slowly and often has no single cause. Risk rises with age, excess sodium intake, obesity, and family history. In most patients no secondary cause is found, and the diagnosis is essential hypertension. Treatment begins with weight loss, reduced salt, and regular aerobic exercise. If readings stay above target, clinicians typically add a thiazide diuretic, an ACE inhibitor, or a calcium channel blocker.",
    "Ibuprofen and warfarin together increase bleeding risk substantially. Ibuprofen inhibits platelet aggregation and irritates the gastric mucosa, while warfarin suppresses vitamin K dependent clotting factors. The combination raises the chance of gastrointestinal haemorrhage. If you need analgesia while anticoagulated, paracetamol is generally preferred. Discuss any new medication with the clinician monitoring your international normalised ratio.",
    "Type two diabetes develops when tissues become resistant to insulin and the pancreas cannot compensate. Early symptoms include increased thirst, frequent urination, fatigue, and blurred vision. Diagnosis uses fasting plasma glucose or glycated haemoglobin. First line management is dietary change and physical activity, with metformin added when glycaemic targets are not met.",
    "Migraine is a neurological disorder, not simply a severe headache. Attacks often involve unilateral throbbing pain, nausea, and sensitivity to light and sound. Roughly a quarter of patients experience aura beforehand. Acute treatment uses triptans or nonsteroidal anti inflammatory drugs. Frequent attacks may justify prophylaxis with propranolol, topiramate, or amitriptyline.",
    "Antibiotics treat bacterial infections and have no effect on viruses. Most sore throats, colds, and acute bronchitis are viral, so antibiotics will not shorten them. Unnecessary prescribing drives antimicrobial resistance and disturbs the gut microbiome. Clinicians may use a rapid streptococcal test to decide whether treatment is warranted.",
    "Asthma causes reversible narrowing of the airways through inflammation and bronchoconstriction. Typical features are wheeze, cough, and breathlessness that worsen at night. Diagnosis rests on spirometry showing reversible obstruction. Management follows a stepwise approach, starting with an inhaled corticosteroid and adding a long acting beta agonist if control remains poor.",
    "Statins reduce cardiovascular events by inhibiting hydroxymethylglutaryl coenzyme A reductase, lowering hepatic cholesterol synthesis. Muscle aches are the most commonly reported adverse effect, though randomised trials suggest true myopathy is uncommon. Rhabdomyolysis is rare. Liver enzymes are usually checked before starting therapy and again after a few months.",
    "Iron deficiency anaemia produces fatigue, pallor, breathlessness on exertion, and sometimes unusual cravings. It is confirmed by a low ferritin alongside reduced haemoglobin and mean corpuscular volume. In adults the underlying cause must be investigated, since occult gastrointestinal blood loss can indicate malignancy. Oral iron replacement is standard.",
    "Atrial fibrillation is an irregular supraventricular rhythm that raises stroke risk roughly fivefold. Patients may report palpitations, breathlessness, or nothing at all. Management has two strands, rate or rhythm control and anticoagulation. Stroke risk is estimated with a validated scoring system, and direct oral anticoagulants have largely replaced warfarin.",
    "Vitamin D is synthesised in skin exposed to ultraviolet B radiation and obtained from oily fish and fortified foods. Deficiency is common at higher latitudes during winter. Severe deficiency causes rickets in children and osteomalacia in adults. Supplementation is recommended for people with limited sun exposure, though very high doses provide no additional benefit.",
    "Depression is diagnosed when low mood or loss of interest persists for at least two weeks alongside disturbance of sleep, appetite, concentration, or energy. Both psychological therapy and antidepressant medication are effective. Selective serotonin reuptake inhibitors are usually first line. Response takes several weeks, and stopping abruptly can cause discontinuation symptoms.",
    "Osteoarthritis results from progressive loss of articular cartilage with secondary bone remodelling. It commonly affects knees, hips, and hands, causing pain that worsens with use. Radiographs show joint space narrowing and osteophytes. Core treatment is exercise and weight management, with topical or oral analgesia and eventual joint replacement.",
    "A stroke occurs when blood supply to part of the brain is interrupted, either by occlusion or by haemorrhage. Sudden facial droop, arm weakness, or speech disturbance should prompt emergency assessment. Imaging distinguishes ischaemic from haemorrhagic stroke. Thrombolysis or thrombectomy can restore perfusion if given quickly.",
    "Coeliac disease is an immune reaction to gluten that damages the small intestinal mucosa. Presentation ranges from diarrhoea and weight loss to isolated anaemia or fatigue. Serological testing for tissue transglutaminase antibodies is the initial investigation, performed while still eating gluten. Duodenal biopsy confirms villous atrophy, and lifelong gluten exclusion is the only treatment.",
    "Chronic kidney disease is staged by estimated glomerular filtration rate and albuminuria. Diabetes and hypertension are the leading causes worldwide. Progression is often silent until function falls substantially. Blood pressure control, renin angiotensin system blockade, and more recently sodium glucose cotransporter inhibitors slow decline.",
    "Antibiotic resistance emerges when bacteria acquire mutations or mobile genetic elements that neutralise a drug. Overuse in medicine and agriculture accelerates the process. Resistant organisms such as meticillin resistant staphylococcus aureus complicate routine procedures. Stewardship programmes restrict broad spectrum agents and shorten courses where evidence supports it.",
    "Thyroid hormone regulates basal metabolic rate, and deficiency produces fatigue, cold intolerance, constipation, and weight gain. Hypothyroidism is usually autoimmune, caused by chronic lymphocytic thyroiditis. Diagnosis rests on a raised thyroid stimulating hormone with low free thyroxine. Levothyroxine replacement is titrated against repeat measurements.",
    "Pneumonia is infection of the lung parenchyma, presenting with fever, productive cough, pleuritic pain, and breathlessness. Severity scoring guides whether a patient needs admission. Chest radiography shows consolidation. Empirical antibiotics are chosen by likely organism and local resistance, with amoxicillin common for uncomplicated community acquired disease.",
    "Eczema, or atopic dermatitis, is a chronic inflammatory skin condition driven by barrier dysfunction and immune activation. It presents with dry itchy skin in flexural areas and often coexists with asthma and hay fever. Emollients applied generously are the foundation of care, with topical corticosteroids used in short courses for flares.",
    "Gastro oesophageal reflux occurs when the lower oesophageal sphincter relaxes inappropriately, allowing acid into the oesophagus. Heartburn and regurgitation are typical. Weight loss, smaller meals, and avoiding late eating help. Proton pump inhibitors suppress acid effectively, but long term use warrants periodic review and attempts at dose reduction.",
    "Sepsis is life threatening organ dysfunction caused by a dysregulated response to infection. Early features are subtle, including tachycardia, confusion, and reduced urine output. Prompt recognition matters more than any single intervention. Blood cultures, broad spectrum antibiotics, and intravenous fluids should be delivered within the first hour.",
    "Osteoporosis reduces bone mineral density and microarchitectural integrity, raising fracture risk at the hip, spine, and wrist. It is often silent until a fragility fracture occurs. Dual energy absorptiometry quantifies density. Adequate calcium and vitamin D, resistance exercise, and bisphosphonate therapy reduce subsequent fractures.",
]

GEN = [
    "Risotto needs constant attention but rewards it. Toast the arborio rice in butter until the grains look translucent at the edges, then add warm stock one ladle at a time. Stir often so the starch releases and the texture turns creamy. The rice should stay slightly firm in the centre. Finish off the heat with cold butter and grated cheese.",
    "Spring and autumn are the most comfortable seasons to visit Japan. Cherry blossom draws enormous crowds in late March and early April, and prices climb accordingly. Autumn brings clear skies and maple colour without quite the same crush. Summer is hot and humid, while winter suits skiing in the north. Book accommodation early for either peak.",
    "Sourdough depends on a live starter rather than commercial yeast. Feed equal weights of flour and water daily until the culture doubles predictably. Mix the dough, rest it, then develop strength with periodic folds instead of kneading. A long cold proof in the refrigerator improves flavour and makes the timing easier to manage.",
    "Learning guitar goes faster if you practise deliberately rather than simply playing. Spend the first minutes on something slightly beyond your current ability, with a metronome set slow enough to stay accurate. Short daily sessions beat occasional long ones. Record yourself occasionally, because your ears miss things your phone will not.",
    "Houseplants usually die from overwatering rather than neglect. Let the top few centimetres of compost dry before watering again, and make sure the pot actually drains. Most species tolerate less light than people assume but resent cold draughts. Repot when roots circle the base, choosing a container only slightly larger.",
    "Compost works fastest when you balance green and brown material. Grass clippings and vegetable peelings supply nitrogen, while cardboard, dry leaves, and straw supply carbon. Aim for roughly equal volumes and turn the heap to keep it aerated. A hot heap breaks down in weeks, a cold one takes most of a year.",
    "Photographing at night needs a stable camera far more than an expensive one. Use a tripod, set a low sensitivity to limit noise, and let the shutter stay open for several seconds. Focus manually on a distant bright point, since autofocus struggles in darkness. Shoot in raw so you can lift shadows later without banding.",
    "Bicycle gears exist to keep your pedalling cadence roughly constant as the terrain changes. Spinning a lighter gear quickly is usually kinder to your knees than grinding a heavy one. Shift before the hill rather than partway up it, and ease the pressure on the pedals as the chain moves across the cassette.",
    "Bread flour differs from plain flour mainly in protein content, which determines how much gluten can form. Higher protein gives a chewier crumb and better rise, which suits loaves and pizza. Plain flour produces a softer result that works better for cakes and pastry. Substituting one for the other changes texture noticeably.",
    "Chess improvement at the beginner stage comes mostly from avoiding blunders rather than studying openings. Before every move, check what your opponent threatened with their last one. Develop pieces toward the centre, castle early, and avoid moving the same piece repeatedly. Tactics puzzles build the pattern recognition that decides most games.",
    "Coffee extraction depends on grind size, water temperature, and contact time. Too coarse a grind or too short a brew tastes sour and thin, because extraction is incomplete. Too fine or too long tastes bitter and harsh. Adjust one variable at a time, and weigh both the grounds and the water for consistency.",
    "Running injuries often trace back to increasing distance too quickly. A common guideline is to add no more than a tenth of your weekly mileage at a time, with an easier week every fourth. Most of your running should feel conversational. Strength work for hips and calves prevents a surprising share of problems.",
    "Wool stays warm when damp because its fibres trap air even after absorbing moisture, unlike cotton which holds water against the skin. Merino is fine enough to wear next to the body without itching. Wash it gently in cool water and dry it flat, since heat and agitation cause the scales to felt together.",
    "Sleep quality improves more from consistency than from any gadget. Going to bed and waking at similar times anchors your circadian rhythm. Keep the room cool and genuinely dark, and get daylight in the morning. Caffeine has a long half life, so an afternoon cup can still be active when you try to sleep.",
    "Rechargeable batteries degrade fastest when kept at very high or very low charge, especially when warm. Storing a device at full charge for months shortens its usable life. For long storage, leave lithium cells around half charged and keep them somewhere cool. Frequent shallow discharges are gentler than repeated deep ones.",
    "Knife sharpening is mostly about maintaining a consistent angle against the stone. Most kitchen knives suit something near fifteen or twenty degrees per side. Work one side until a slight burr forms along the whole edge, then match it on the other. Finish on a finer stone and strop to remove the remaining burr.",
    "Tomatoes grown outdoors need sun, steady moisture, and support as they climb. Irregular watering causes the fruit to split or develop dark patches at the base. Pinch out side shoots on vine varieties to concentrate energy in the main stem. Feed with a high potassium fertiliser once the first fruits set.",
    "Public speaking nerves fade faster with preparation than with willpower. Know your opening two sentences well enough to deliver them automatically, because that is when anxiety peaks. Speak slower than feels natural and pause at the ends of sentences. Looking at individual faces rather than the whole room helps steady you.",
    "Wood glue joints are usually stronger than the surrounding timber when the surfaces mate well. Clamping pressure matters less than good contact and even spread. End grain absorbs glue and bonds poorly, which is why joinery uses mechanical interlocks. Wipe squeeze out before it cures, since dried glue rejects stain.",
    "Cast iron pans work best when the seasoning is maintained rather than restored. Heat the dry pan, add a very thin film of oil, and wipe almost all of it away before heating further. Thick coatings turn sticky instead of hardening. Acidic sauces and long soaking strip the layer you have built.",
    "Time zones exist because solar noon differs with longitude, and railways made local timekeeping unworkable. Most zones sit an hour apart, though several use half hour or quarter hour offsets. Daylight saving shifts clocks seasonally in some countries but not others, which is why the difference between two cities changes during the year.",
    "Soldering a clean joint needs heat applied to the parts rather than the solder itself. Tin the iron, bring it against both the pad and the component lead, then feed solder into the joint so it flows by capillary action. A good joint looks shiny and concave. Flux removes oxide and makes wetting reliable.",
]



# --- tokenizers -------------------------------------------------------------
# ws  : whitespace "words" (the original synthetic assumption)
# bpe : real subword tokens from tiktoken cl100k_base. These differ sharply:
#       rare medical words shatter into several short pieces ("Hypertension"
#       -> H|yp|ert|ension) while common words are one piece with a leading
#       space. Stage 2 tests whether that changes the side channel.

_ENC = None


def ws(text):
    return text.split()


def bpe(text):
    global _ENC
    if _ENC is None:
        import tiktoken
        _ENC = tiktoken.get_encoding("cl100k_base")
    return [_ENC.decode([t]) for t in _ENC.encode(text)]


def _cands(texts, tmin, tmax, tok):
    """Every contiguous token-window, as (src_idx, n_tokens, n_chars, start)."""
    out = []
    for i, t in enumerate(texts):
        toks = tok(t)
        for n in range(tmin, min(tmax, len(toks)) + 1):
            for s in range(0, len(toks) - n + 1):
                out.append((i, n, sum(len(x) for x in toks[s:s + n]), s))
    return out


def matched_samples(tok=ws, tol_char=0.02, tmin=32, tmax=44, per_text=4,
                    per_n=99):
    """Pair MED and GEN token-windows with IDENTICAL token count and character
    length within tol_char, so chunk count, total bytes and total duration
    carry no class information by construction.

    Windows rather than prefixes: matching both axes is only possible with a
    large candidate pool, because mean token length is itself a class
    signature (MED runs ~9% longer per whitespace token).
    """
    mt = {i: tok(t) for i, t in enumerate(MED)}
    gt = {i: tok(t) for i, t in enumerate(GEN)}
    mby, gby = {}, {}
    for mi, n, c, s in _cands(MED, tmin, tmax, tok):
        mby.setdefault(n, []).append((mi, c, s))
    for gi, n, c, s in _cands(GEN, tmin, tmax, tok):
        gby.setdefault(n, []).append((gi, c, s))
    um, ug, pairs = {}, {}, []
    for n in sorted(mby):
        made = 0
        for mi, mc, ms in sorted(mby[n], key=lambda r: um.get(r[0], 0)):
            if um.get(mi, 0) >= per_text or made >= per_n:
                continue
            best, bestd = None, None
            for gi, gc, gs in gby.get(n, []):
                if ug.get(gi, 0) >= per_text:
                    continue
                d = (abs(gc - mc) / max(mc, 1), ug.get(gi, 0))
                if d[0] <= tol_char and (bestd is None or d < bestd):
                    best, bestd = (gi, gc, gs), d
            if best:
                um[mi] = um.get(mi, 0) + 1
                ug[best[0]] = ug.get(best[0], 0) + 1
                made += 1
                pairs.append({
                    "n_tokens": n, "med_src": mi, "gen_src": best[0],
                    "med_chars": mc, "gen_chars": best[1],
                    "med_toks": mt[mi][ms:ms + n],
                    "gen_toks": gt[best[0]][best[2]:best[2] + n],
                })
    return pairs


def count_matched(n_tokens=40, tok=ws):
    """Condition A: every text truncated to EXACTLY n_tokens.

    Chunk count and duration are identical across all samples; total bytes is
    free to differ. Uses the whole corpus, so the group-aware split gets 44
    distinct groups.
    """
    out = []
    for lab, texts in (("MED", MED), ("GEN", GEN)):
        for i, t in enumerate(texts):
            toks = tok(t)
            if len(toks) >= n_tokens:
                out.append({"label": lab, "group": f"{lab}{i}",
                            "toks": toks[:n_tokens]})
    return out


def byte_matched(tok=ws, **kw):
    """Condition B: token count AND character length both matched (strict)."""
    out = []
    for p in matched_samples(tok=tok, **kw):
        out.append({"label": "MED", "group": f"MED{p['med_src']}",
                    "toks": p["med_toks"]})
        out.append({"label": "GEN", "group": f"GEN{p['gen_src']}",
                    "toks": p["gen_toks"]})
    return out


def full_corpus(tok=ws):
    """Unmatched: whole responses, variable length (the easy-channel case)."""
    return [{"label": lab, "group": f"{lab}{i}", "toks": tok(t)}
            for lab, ts in (("MED", MED), ("GEN", GEN))
            for i, t in enumerate(ts)]
