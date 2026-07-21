# Proposal

# Final Proposal

**Team Members:** Mingzhu Li, Xinwei Song, Yuqi Wei, Peng Yu

**Working Direction / Title:** Learning Useful Representations Through Prediction for Streaming RL

**What do you want to understand?**

We want to understand whether representations learned through predictive tasks can become useful state for online decision making under partial observability and non\-stationary\.

The Alberta Plan emphasizes predictive knowledge as central to agent state, but "learning a prediction" and "learning a useful representation through prediction" are different\. A prediction can be accurate yet carry no information about the hidden variable needed for control; or it can carry weak hidden information yet fail to improve downstream decisions\.

The core research question: Under the streaming, replay\-free linear RL constraint for continuing POMDPs, what conditions make a predictive GVF task yield representations that simultaneously satisfy two critical properties:

\(a\) the latent decision\-critical hidden information is reliably preserved at action selection steps;

\(b\) the encoded representation delivers measurable performance gains for downstream control policy learning\.

**What setting or testbed will you use?**

We will use a continuing partially observable T\-maze:

- A binary cue appears at the start of each trial, then is hidden during a corridor\.

- At the delayed junction, the correct action depends on the initial cue\.

- Raw observation at the junction is aliased—the agent must retain the cue through the corridor\.

- The task is continuing: trials repeat without resetting the agent's weights, memory, or learned predictions\.

**What will you examine?**

We will compare representations formed from different predictive tasks \(cumulants: cue, terminal outcome, junction signal\) and horizons\.

All agents use online linear learning with no replay buffer, no deep network, and no offline fitting\.

The key examination is:

- At decision time, does the learned representation still encode the hidden cue?

- Does this representation improve the agent's decisions over raw observation?

**What will you look at?**

We will look for evidence that separates prediction accuracy from representation usefulness:

- Trial accuracy: Does the representation improve task performance?

- Cue decodability: Does the representation still contain the hidden variable at decision time?

- Cue\-alignment margin: How strongly does the representation separate cue=left vs cue=right?

- Prediction TD error

The main expected figure plots trial accuracy and cue decodability by maze length, predictive task, and horizon\.

# 余鹏 mark

继续深入调研 Agent state and representation 和 Planning

# Xinwei

Idea 1

What do you want to understand?

Can we design an "intentional" update rule for the eligibility trace parameter \\lambda, analogous to how intentional updates choose step\-size based on functional outcomes, that makes \\lambda adapt online in non\-stationary streaming environments?



What setting or testbed will you use?

- Primary: Non\-stationary linear regression \(Alberta Plan Step 1 setting\), where the target weights drift over time\.

- Extension: Two\-loop or cycle MDP \(continuing, average\-reward\) to test how adaptive lambda affects prediction error in a streaming RL setting\.



What will you examine?

- Baseline: Fixed lambda TD\(lambda\) with Intentional TD step\-size\.

- Variation: Replace fixed lambda with an online adaptive rule, e\.g\., choose lambda to balance the propagation of TD error over past states, making the effective update footprint proportional to the current prediction error\.

- Compare fixed and adaptive lambda under varying drift rates\.



What will you look at?

- Tracking error \(MSE\) over time\. Does adaptive lambda recover faster than the best fixed one under abrupt drift?

- lambda\_t trajectory\. Does it decrease when drift is high \(short memory\) and increase when drift is low \(long memory\)?

- Sensitivity to meta\-parameters\. How robust is the adaptive rule compared to tuning lambda by hand?



idea 2

What do you want to understand?

Can we implement a streaming, generate\-and\-test feature discovery mechanism — in the spirit of Alberta Plan Step 2 — that adds new features to a linear value function approximator without introducing auxiliary gradient losses that interfere with the primary RL update?



What setting or testbed will you use?

- Primary: Non\-stationary linear regression \(Alberta Plan Step 1 setting\) with a fixed linear feature set, then extended to allow generation of new nonlinear features \(e\.g\., products of existing features, thresholded versions, random combinations\)\.

- Extension: Two\-loop MDP or non\-stationary gridworld, where the linear value function needs to adapt to changing dynamics, and new features are generated to capture the changing structure\.



What will you examine?

- Baseline: TD with a fixed feature representation\.

- Extension: Add a feature generation \& testing loop:

    1. Generate: Periodically \(or based on TD error triggers\), generate candidate features \(from existing ones\)\.

    2. Test: For each candidate, compute its utility — the reduction in TD error it would bring if added to the linear model \(using a simple one\-step correlation or gradient test\)\.

    3. Add/Replace: If a candidate's utility exceeds a threshold, add it to the feature set  \(or maybe we can apply some game theory approaches like the shapley value to estimate the importance of each representation\); if the feature set exceeds capacity, replace the lowest\-utility feature\.

    https://arxiv\.org/pdf/2605\.15877

- Compare: Fixed features vs\. generate\-and\-test feature set under varying drift rates\.



What will you look at?

- Tracking error \(MSE\) over time\. Does generate\-and\-test recover faster than fixed features under abrupt drift?

- Feature set composition over time\. Show which features survive and which are replaced\. Does the set evolve to match the changing target function?

- Feature utility histogram: distribution of utilities across the feature set before and after drift\. This directly visualizes why generate\-and\-test works — under drift, old features lose utility and new ones gain it\.

- Tracking error vs\. number of features tested\. How many candidates do you need to generate per step to match the performance of a handcrafted oracle feature set? This speaks to computational cost and efficiency\.



# 李明珠

Add Fixed\-Capacity Online Episodic Memory with GVF\-Based Predictive State Construction in a Continuing Survival Environment

\[Proposal \- Online Episodic Memory and GVFs\.md\]
