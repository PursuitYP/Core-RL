# Literature Notes

This note is a working bibliography for the Alberta Plan Core RL project. It should be
updated as experiments expose sharper questions.

## Alberta Plan Lens

- The Alberta Plan: https://arxiv.org/abs/2208.11173  
  Core framing: long-lived agents learn from ordinary experience, with temporal uniformity,
  limited computation, online prediction/control, learned models, planning, GVFs, feature
  finding, options, STOMP, and Oak-style utility feedback.

- Rethinking the Foundations for Continual RL: https://arxiv.org/abs/2504.08161  
  Supports process metrics over final artifacts: online error, recovery time, regret over
  a stream, feature utility, and adaptation.

- A Definition of Continual RL: https://arxiv.org/abs/2307.11046  
  Supports the idea that good agents do not stop learning.

## Reward Centering and Average Reward

- Reward Centering: https://arxiv.org/abs/2405.09999  
  Main source for Reward-Centered Continuing Sarsa. It shows that subtracting empirical
  average reward improves continuing discounted methods and removes constant reward-shift
  sensitivity.

- Learning and Planning in Average-Reward MDPs: https://arxiv.org/abs/2006.16318  
  Useful for differential TD/Q-learning mechanics and average-reward planning.

- Extending Differential TD Methods for Episodic Problems: https://arxiv.org/abs/2605.04368  
  Warns that naive centering can alter policy ordering in episodic tasks. Keep reward
  centering claims focused on continuing tasks.

- Bellman Error Centering: https://arxiv.org/abs/2502.03104  
  Useful diagnostic distinction: simple reward centering and Bellman-error centering remove
  related but not identical offsets.

Implementation implication: report unshifted task reward separately from shifted observed
reward. Otherwise reward shifts fake better curves.

## Streaming TD, Normalization, and Plasticity

- Streaming Deep RL Finally Works: https://arxiv.org/abs/2410.14606  
  Motivates the stream barrier: no replay, no target-network smoothing, batch size 1.
  Translate to linear settings through traces, normalization, and controlled update scale.

- Intentional Updates for Streaming RL: https://arxiv.org/abs/2604.19033  
  Main source for Output-Controlled TD. Step-size should control output change, not just
  parameter movement. Linear TD(0) reduces naturally to normalized TD.

- True Online TD Learning: https://arxiv.org/abs/1512.04087  
  Strong non-deep trace baseline with exact online forward-view equivalence for TD(lambda)
  and Sarsa(lambda).

- TIDBD: https://arxiv.org/abs/1804.03334  
  Per-feature TD step-size adaptation. Use as contrast with output-controlled TD:
  TIDBD adapts parameter step-sizes; normalized/intentional TD controls prediction change.

- Maintaining Plasticity in Deep Continual Learning: https://arxiv.org/abs/2306.13812  
  Mostly deep, but motivates plasticity diagnostics: feature-wise step-sizes, recovery after
  drift, and whether normalization reduces retuning.

## GVFs and Agent State

- What's a Good Prediction?: https://arxiv.org/abs/2001.08823  
  Prediction accuracy is not enough; evaluate predictions by usefulness to learning and
  behavior.

- Finding Useful Predictions: https://arxiv.org/abs/2111.11212  
  Shows the possibility of selecting predictions that resolve partial observability.

- Horde / lifelong off-policy GVFs: https://arxiv.org/abs/1206.6262  
  Useful background for GVFs at scale. The current project keeps GVFs on-policy unless
  explicitly studying off-policy stability.

## Representation, Options, and Planning

- Learning Agent State Online with Recurrent Generate-and-Test: https://arxiv.org/abs/2112.15236  
  Main source for generate-and-test trace features under partial observability.

- The Option-Critic Architecture: https://arxiv.org/abs/1609.05140  
  Background for options. The project uses hand-coded doorway options as a minimal
  reusable-subtask test, not option discovery.

- Dyna, planning, and prioritized sweeping are part of the Alberta Plan planning line.
  For this project, Dyna stores a compact model, not a raw replay buffer.

## Additional Search Round: Design Corrections

This search round focused on sources that directly correct experiment design rather than on
expanding the bibliography.

- Reward Centering and average-reward planning support moving the main reward-centering
  experiment to access-control queue. The two-loop MDP remains a mechanism illustration.
- Intentional Updates, Streaming Deep RL, and Squeezing More from the Stream support treating
  normalized TD as a small linear proxy for output-controlled updates. This led to the
  tile-coded random-walk main setting and alpha-by-scale stability grid.
- Finding Useful Predictions and Recurrent Generate-and-Test support evaluating GVFs by
  downstream state usefulness, not prediction accuracy alone. This led to raw/history/GVF/oracle
  baselines in a longer aliased T-maze.
- Options and Dyna classic work support evaluating temporal abstraction and model planning
  by real environment-step cost and model staleness, not by decision-step curves alone.
- Baird/TDC/GTD/ETD literature supports keeping Baird as an off-policy stability diagnostic
  unless the canonical setup is verified carefully enough for a main claim.

Current design consequence:

- Final story should be narrowed. Reward-Centered Sarsa and Output-Controlled TD are the
  strongest main studies after current pilots.
- GVF predictive state and feature plasticity need another design round before they can carry
  main conclusions.
- Options, Baird, and Dyna are useful supporting studies or appendices.
