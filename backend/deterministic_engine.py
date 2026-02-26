import re
from typing import Set, Dict, Tuple, List

from skills import (
    ROLES,
    SKILL_ALIASES,
    SKILL_HIERARCHY
)


# ================================
# TEXT NORMALIZATION
# ================================

def normalize_text(text: str) -> str:
    if not text:
        return ""
    text = text.lower()
    text = re.sub(r"[^a-z0-9\+\#\./]", " ", text)
    return text


# ================================
# SKILL EXTRACTION
# ================================

def extract_skills(resume_text: str) -> Set[str]:
    resume_text = normalize_text(resume_text)
    detected = set()

    # 1️⃣ Alias detection (primary detection layer)
    for canonical_skill, aliases in SKILL_ALIASES.items():
        for alias in aliases:
            if re.search(rf"\b{re.escape(alias)}\b", resume_text):
                detected.add(canonical_skill)
                break

    # 2️⃣ Hierarchy propagation (graph expansion)
    expanded = set(detected)

    for skill in list(detected):
        parent = SKILL_HIERARCHY.get(skill)
        while parent:
            expanded.add(parent)
            parent = SKILL_HIERARCHY.get(parent)

    return expanded


# ================================
# ROLE SCORING
# ================================

def calculate_role_score(
    user_skills: Set[str],
    role_data: Dict
) -> Tuple[int, List[str], List[str]]:

    total_weight = 0
    matched_weight = 0

    core_total = 0
    core_matched = 0

    matched = []
    missing = []

    for category in ["core", "supporting", "bonus"]:
        skills = role_data.get(category, {})

        for skill, weight in skills.items():
            total_weight += weight

            if category == "core":
                core_total += weight

            if skill in user_skills:
                matched_weight += weight
                matched.append(skill)

                if category == "core":
                    core_matched += weight
            else:
                missing.append(skill)

    score = int((matched_weight / total_weight) * 100) if total_weight else 0

    # 🔒 Core enforcement
    if core_total > 0:
        core_ratio = core_matched / core_total
        if core_ratio < 0.4:
            score = min(score, 50)

    # 🔥 Apply demand multiplier
    demand_weight = role_data.get("metadata", {}).get("demand_weight", 1.0)
    score = int(score * demand_weight)

    return score, matched, missing


# ================================
# COMPOSITE ROLE LOGIC
# ================================

def compute_composite_roles(results):

    role_map = {r["role"]: r for r in results}

    if "Backend Developer" in role_map and "Frontend Developer" in role_map:
        backend_score = role_map["Backend Developer"]["score"]
        frontend_score = role_map["Frontend Developer"]["score"]

        fullstack_score = int((backend_score + frontend_score) / 2)

        # Penalize imbalance
        difference = abs(backend_score - frontend_score)
        if difference > 30:
            fullstack_score -= 10

        results.append({
            "role": "Full Stack Developer",
            "score": fullstack_score,
            "matched_skills": list(
                set(role_map["Backend Developer"]["matched_skills"] +
                    role_map["Frontend Developer"]["matched_skills"])
            ),
            "missing_skills": [],
            "improvement_steps": []
        })

    return results


# ================================
# BEST FIT LOGIC
# ================================

def determine_best_fit(results):

    if len(results) < 2:
        return results[0]["role"]

    top1 = results[0]
    top2 = results[1]

    if abs(top1["score"] - top2["score"]) <= 5:
        return f"Hybrid: {top1['role']} + {top2['role']} (leaning {top1['role']})"

    return top1["role"]


# ================================
# FULL EVALUATION
# ================================

def deterministic_evaluation(resume_text: str) -> Dict:

    user_skills = extract_skills(resume_text)

    results = []

    for role in ROLES:
        role_name = role["name"]

        score, matched, missing = calculate_role_score(
            user_skills,
            role
        )

        results.append({
            "role": role_name,
            "score": score,
            "matched_skills": matched,
            "missing_skills": missing,
            "improvement_steps": generate_improvement_steps(missing)
        })

    results = compute_composite_roles(results)
    results.sort(key=lambda x: x["score"], reverse=True)

    best_fit = determine_best_fit(results)

    return {
        "roles": results,
        "best_fit": best_fit,
        "summary": "Deterministic ontology-driven role alignment"
    }


# ================================
# IMPROVEMENT GENERATION
# ================================

def generate_improvement_steps(missing_skills: List[str]) -> List[str]:
    steps = []
    for skill in missing_skills[:3]:
        steps.append(f"Improve proficiency in {skill}")
    return steps