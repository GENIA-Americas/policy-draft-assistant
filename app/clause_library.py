"""
Deterministic clause library. This is a template engine, not a call out to a
generative model: every clause below is fixed text assembled based on selections.
If you want actual LLM-drafted language later, that's a separate integration
(e.g. calling the Anthropic API) layered on top of this — not built here.
"""

CLAUSES: dict[str, dict[str, str]] = {
    "acceptable_use": {
        "no_confidential_input": (
            "Employees must not input confidential, proprietary, or personally "
            "identifiable information into any external AI tool without prior "
            "written approval from the Data Governance team."
        ),
        "human_review_required": (
            "Any AI-generated output used in external communications, legal "
            "documents, or financial reporting must be reviewed and approved by "
            "a qualified human before use."
        ),
        "approved_tools_only": (
            "Employees may only use AI tools that appear on the organization's "
            "approved tools list, maintained by IT Security."
        ),
        "no_automated_decisions": (
            "AI systems must not be used to make final decisions about hiring, "
            "termination, credit, or other legally significant matters without "
            "human review."
        ),
    },
    "data_governance": {
        "data_minimization": (
            "Only the minimum data necessary for a given AI use case shall be "
            "collected, processed, or retained."
        ),
        "retention_limits": (
            "Data used in AI training or inference shall be retained no longer "
            "than necessary for the stated purpose, and in line with the "
            "organization's data retention schedule."
        ),
        "access_controls": (
            "Access to datasets used for AI development shall be restricted to "
            "authorized personnel and logged for audit purposes."
        ),
        "third_party_data_sharing": (
            "Data may not be shared with third-party AI vendors unless a data "
            "processing agreement is in place."
        ),
    },
    "vendor_risk": {
        "vendor_security_review": (
            "All AI vendors must complete a security review prior to onboarding, "
            "covering data handling, model training practices, and incident "
            "response."
        ),
        "sla_uptime_requirements": (
            "AI vendor contracts must specify minimum uptime and support "
            "response-time commitments appropriate to the criticality of the "
            "use case."
        ),
        "exit_and_portability": (
            "Contracts with AI vendors must include data export and portability "
            "provisions to avoid vendor lock-in."
        ),
        "liability_allocation": (
            "Contracts must clearly allocate liability for harms arising from "
            "AI system errors, bias, or data breaches."
        ),
    },
}


def available_clauses(policy_type: str) -> dict[str, str]:
    return CLAUSES.get(policy_type, {})


def render_policy(org_name: str, policy_type: str, clause_keys: list[str]) -> str:
    library = available_clauses(policy_type)
    lines = [f"# {policy_type.replace('_', ' ').title()} Policy", "", f"Organization: {org_name}", ""]
    for i, key in enumerate(clause_keys, start=1):
        text = library.get(key)
        if text is None:
            continue
        lines.append(f"{i}. {text}")
    return "\n".join(lines)
