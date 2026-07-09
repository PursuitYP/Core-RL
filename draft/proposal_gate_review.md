# Proposal Gate Review Notes

The final-facing gate is in `final/archive/legacy/proposal_gate_review.md`. This draft note
records why the gate was added.

Multi-role critique found that the project was too broad and that some proposal dossiers
still reflected early minimal runs. The gate prevents the project from getting stuck in weak
topics by requiring each proposal to earn promotion through:

1. A focused Core-RL question.
2. Alberta Plan relevance.
3. Streaming/no-replay/no-deep compliance.
4. A non-toy or canonical main setting.
5. Baselines that isolate the mechanism.
6. Seed-aware metrics that actually answer the question.

Current decision: Reward-Centered Sarsa and Output-Controlled TD are the main stories.
Dyna is the only plausible compact third story after the recovery-window rerun, but its
claim must be model staleness/recovery rather than generic planning speed. GVF remains a
redesign/negative result, TIDBD is mechanism-only support, Generate-and-Test is downgraded
to a failed current design unless redesigned, and Baird/options are supporting or
quarantined material.
