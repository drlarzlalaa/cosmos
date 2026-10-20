#!/usr/bin/env python3
"""Generate the COSMOS directory scaffold from TREE below.

Idempotent and safe to re-run: it only ever writes a placeholder
README.md into a leaf directory if that directory has no README.md
yet, so it never overwrites real code or a README someone has since
written by hand. Run from the repo root: python3 tools/generate_scaffold.py
"""
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# (top_dir, purpose, phase, [leaf, ...])
# "purpose" is taken verbatim from ARCHITECTURE.md's Purpose: lines for
# that section. "phase" is the ROADMAP.md phase that first touches it.
TREE = [
    ("frontend", "Provide the interface for exploring the universe, conducting research, and examining potential universal laws.", 1, [
        "dashboard", "universe-explorer", "cosmic-visualization", "physics-explorer",
        "mathematics-lab", "consciousness-lab", "causality-explorer", "existence-and-origin",
        "spiritual-philosophy", "hypothesis-laboratory", "simulation-workspace",
        "evidence-explorer", "research-library", "discovery-reports",
        "AI-research-assistant", "experiment-manager", "user-workspaces", "settings",
    ]),
    ("backend", "Manage application operations, coordinate research tasks, and connect the frontend to the scientific engines.", 1, [
        "api-gateway", "authentication", "authorization", "user-management",
        "research-orchestrator", "task-management", "workflow-engine",
        "notification-service", "experiment-management", "hypothesis-management",
        "report-generation", "search-service", "audit-logging", "configuration",
    ]),
    ("engines/physics-engine", "Investigate different dimensions of reality through specialised research systems.", 3, [
        "gravity", "relativity", "quantum-mechanics", "electromagnetism",
        "thermodynamics", "cosmology",
    ]),
    ("engines/mathematics-engine", "Investigate different dimensions of reality through specialised research systems.", 3, [
        "algebra", "calculus", "geometry", "probability", "symmetry-analysis",
        "symbolic-regression",
    ]),
    ("engines/cosmic-data-engine", "Investigate different dimensions of reality through specialised research systems.", 3, [
        "galaxy-analysis", "stellar-analysis", "gravitational-wave-analysis",
        "cosmic-background-analysis", "astronomical-anomaly-detection",
    ]),
    ("engines/consciousness-engine", "Investigate different dimensions of reality through specialised research systems.", 6, [
        "neuroscience", "cognition", "perception", "neural-signal-analysis",
        "consciousness-theories",
    ]),
    ("engines/causality-engine", "Investigate different dimensions of reality through specialised research systems.", 6, [
        "causal-inference", "correlation-analysis", "causal-graphs",
        "counterfactual-analysis",
    ]),
    ("engines/existence-engine", "Investigate different dimensions of reality through specialised research systems.", 6, [
        "origin-of-universe", "nature-of-reality", "existence-hypotheses",
        "philosophical-analysis",
    ]),
    ("engines/spiritual-research-engine", "Investigate different dimensions of reality through specialised research systems.", 6, [
        "universal-principles", "historical-beliefs", "comparative-philosophy",
        "claim-evidence-analysis",
    ]),
    ("engines/universal-discovery-engine", "Investigate different dimensions of reality through specialised research systems.", 7, [
        "pattern-discovery", "cross-domain-analysis", "hypothesis-generation",
        "mathematical-law-discovery", "competing-theory-analysis",
        "candidate-law-ranking",
    ]),
    ("scientific-methods", "Ensure that potential discoveries are evaluated against evidence rather than accepted because they appear convincing.", 4, [
        "hypothesis-formulation", "mathematical-modelling", "statistical-analysis",
        "experimental-design", "prediction-testing", "uncertainty-quantification",
        "bias-detection", "falsification", "independent-replication",
        "reproducibility", "scientific-review",
    ]),
    ("intelligence", "Coordinate AI-assisted research across all modules. Each agent should have a defined responsibility and share findings through the research orchestrator rather than operate as a disconnected chatbot.", 5, [
        "research-agent", "literature-analysis-agent", "mathematical-reasoning-agent",
        "simulation-agent", "hypothesis-generation-agent", "anomaly-detection-agent",
        "model-comparison-agent", "evidence-evaluation-agent",
        "research-coordination-agent", "scientific-reporting-agent",
    ]),
    ("simulation", "Test mathematical models and explore how different assumptions affect their predictions.", 3, [
        "physical-simulations", "quantum-simulations", "cosmological-simulations",
        "mathematical-simulations", "neural-simulations", "causal-simulations",
        "alternative-models", "parameter-exploration", "simulation-validation",
    ]),
    ("data-platform", "Store the observations, research papers, mathematical models, and experimental results required by the system.", 2, [
        "data-ingestion", "scientific-data-connectors", "data-validation",
        "data-normalization", "metadata-management", "scientific-datasets",
        "research-paper-index", "hypothesis-registry", "observation-registry",
        "experiment-registry", "model-registry", "data-provenance",
    ]),
    ("knowledge-graph", "Map relationships between concepts, observations, theories, and hypotheses - for example connecting gravity to spacetime curvature, the mathematical models involved, and the observations supporting them. It must also record when a relationship is speculative rather than established.", 7, [
        "entities", "scientific-concepts", "mathematical-relationships",
        "physical-laws", "consciousness-theories", "philosophical-claims",
        "hypotheses", "supporting-evidence", "contradictory-evidence",
        "relationship-discovery",
    ]),
    ("storage", "Preserve structured research data, scientific files, and relationships between discoveries.", 1, [
        "relational-database", "scientific-data-storage", "knowledge-graph-database",
        "vector-database", "time-series-storage", "experiment-results",
        "simulation-results", "backup-and-recovery",
    ]),
    ("discovery", "Turn research results into findings that can be examined, challenged, and reproduced. Every candidate discovery should include its mathematical formulation, supporting observations, assumptions, uncertainty, competing explanations, and validation status.", 8, [
        "candidate-discoveries", "mathematical-equations", "discovered-patterns",
        "prediction-results", "anomaly-reports", "competing-explanations",
        "evidence-strength-assessment", "replication-status", "discovery-history",
    ]),
    ("infrastructure", "Make the platform reliable, secure, and scalable.", 8, [
        "deployment", "containerization", "job-queues", "background-workers",
        "compute-management", "resource-monitoring", "logging-and-monitoring",
        "access-control", "secrets-management", "backups", "disaster-recovery",
    ]),
    ("testing", "Testing and quality assurance for every layer of the platform.", 8, [
        "unit-tests", "integration-tests", "API-tests", "mathematical-correctness-tests",
        "scientific-benchmark-tests", "simulation-validation-tests", "data-quality-tests",
        "AI-evaluation", "reproducibility-tests",
    ]),
]

SECTION_README = """# {title}

> Purpose: {purpose}

**Status:** Phase {phase} of 8 — see [ROADMAP.md](../{depth}ROADMAP.md) and
[ARCHITECTURE.md](../{depth}ARCHITECTURE.md) for the full plan.

Sub-modules:
{leaf_list}
"""

LEAF_README = """# {name}

Part of [`{parent}`](../README.md) in the COSMOS platform.

**Status:** Phase {phase} of 8 — not yet implemented.
See [ARCHITECTURE.md](../../{depth}ARCHITECTURE.md) and
[ROADMAP.md](../../{depth}ROADMAP.md) for what this module is for and when
it's planned to land.
"""


def write_if_absent(path, content):
    if os.path.exists(path):
        return False
    with open(path, "w") as f:
        f.write(content)
    return True


def main():
    created = 0
    for top_dir, purpose, phase, leaves in TREE:
        top_path = os.path.join(ROOT, top_dir)
        os.makedirs(top_path, exist_ok=True)
        depth = "../" * (top_dir.count("/"))
        leaf_list = "\n".join("- `%s/`" % leaf for leaf in leaves)
        section_readme = os.path.join(top_path, "README.md")
        if write_if_absent(section_readme, SECTION_README.format(
                title=top_dir, purpose=purpose, phase=phase, depth=depth,
                leaf_list=leaf_list)):
            created += 1
        for leaf in leaves:
            leaf_path = os.path.join(top_path, leaf)
            os.makedirs(leaf_path, exist_ok=True)
            leaf_readme = os.path.join(leaf_path, "README.md")
            if write_if_absent(leaf_readme, LEAF_README.format(
                    name=leaf, parent=top_dir, phase=phase, depth=depth)):
                created += 1
    print("scaffold complete: %d README.md placeholders written (existing files left untouched)" % created)


if __name__ == "__main__":
    main()
