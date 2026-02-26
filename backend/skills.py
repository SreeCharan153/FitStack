# skills.py

# ================================
# 1️⃣ CANONICAL SKILL REGISTRY
# ================================

SKILLS = {
    # Core Languages
    "python": {},
    "sql": {},
    "javascript": {},
    "html": {},
    "css": {},

    # Backend Concepts
    "apis": {},
    "authentication": {},
    "database": {},
    "microservices": {},

    # DevOps / Infra
    "linux": {},
    "docker": {},
    "kubernetes": {},
    "ci/cd": {},
    "cloud": {},
    "aws": {},
    "terraform": {},
    "networking": {},

    # Data
    "data pipelines": {},
    "spark": {},
    "hadoop": {},
    "airflow": {},
    "snowflake": {},
    "dbt": {},

    # Tools
    "redis": {},
    "kafka": {},
    "react": {},
    "typescript": {},
    "next.js": {},
    "tailwind": {},
}

# ================================
# 2️⃣ SKILL HIERARCHY (GRAPH)
# ================================

SKILL_HIERARCHY = {
    "postgresql": "sql",
    "mysql": "sql",
    "sqlite": "sql",

    "mongodb": "database",

    "fastapi": "apis",
    "django": "apis",
    "flask": "apis",

    "rest": "apis",
    "restful": "apis",

    "jwt": "authentication",
    "oauth": "authentication",

    "k8s": "kubernetes",

    "azure": "cloud",
    "gcp": "cloud",
    "aws": "cloud",

    "etl": "data pipelines",
    "pipeline": "data pipelines",

    "node.js": "javascript",
}

# ================================
# 3️⃣ SKILL ALIASES (ROBUST EXTRACTION)
# ================================

SKILL_ALIASES = {
    "python": ["python"],
    "sql": ["sql"],
    "javascript": ["javascript", "js"],
    "html": ["html"],
    "css": ["css"],
    "apis": ["api", "apis", "rest", "restful"],
    "authentication": ["auth", "authentication", "jwt", "oauth"],
    "database": ["database", "db"],
    "microservices": ["microservice", "microservices", "distributed systems"],
    "linux": ["linux"],
    "docker": ["docker", "containerized", "containers"],
    "kubernetes": ["kubernetes", "k8s"],
    "ci/cd": ["ci/cd", "pipeline", "deployment pipeline"],
    "cloud": ["cloud"],
    "aws": ["aws", "amazon web services"],
    "terraform": ["terraform"],
    "networking": ["networking"],
    "data pipelines": ["data pipeline", "data pipelines", "etl"],
    "spark": ["spark"],
    "hadoop": ["hadoop"],
    "airflow": ["airflow"],
    "snowflake": ["snowflake"],
    "dbt": ["dbt"],
    "redis": ["redis"],
    "kafka": ["kafka"],
    "react": ["react"],
    "typescript": ["typescript"],
    "next.js": ["next.js"],
    "tailwind": ["tailwind"],
    "fastapi": ["fastapi"],
    "django": ["django"],
    "flask": ["flask"],
    "azure": ["azure"],
    "gcp": ["gcp"],
}

# ================================
# 4️⃣ ROLE DEFINITIONS
# ================================

ROLES = [
    {
        "name": "Backend Developer",
        "core": {
            "python": 5,
            "sql": 5,
            "apis": 4,
        },
        "supporting": {
            "database": 3,
            "authentication": 3,
            "docker": 2,
            "aws": 2,
        },
        "bonus": {
            "redis": 1,
            "kafka": 1,
            "microservices": 2,
        },
        "metadata": {
            "industry": "Backend",
            "demand_weight": 1.0
        }
    },

    {
        "name": "Frontend Developer",
        "core": {
            "html": 5,
            "css": 5,
            "javascript": 5,
        },
        "supporting": {
            "react": 4,
            "typescript": 3,
        },
        "bonus": {
            "next.js": 2,
            "tailwind": 1,
        },
        "metadata": {
            "industry": "Frontend",
            "demand_weight": 1.0
        }
    },

    {
        "name": "DevOps Engineer",
        "core": {
            "linux": 5,
            "docker": 5,
            "kubernetes": 4,
            "ci/cd": 4,
            "cloud": 4,
        },
        "supporting": {
            "networking": 3,
            "microservices": 2,
        },
        "bonus": {
            "terraform": 2,
        },
        "metadata": {
            "industry": "Infrastructure",
            "demand_weight": 1.0
        }
    },

    {
        "name": "Data Engineer",
        "core": {
            "sql": 5,
            "python": 5,
            "data pipelines": 4,
        },
        "supporting": {
            "spark": 3,
            "airflow": 2,
        },
        "bonus": {
            "snowflake": 2,
            "dbt": 1,
        },
        "metadata": {
            "industry": "Data",
            "demand_weight": 1.1
        }
    }
]