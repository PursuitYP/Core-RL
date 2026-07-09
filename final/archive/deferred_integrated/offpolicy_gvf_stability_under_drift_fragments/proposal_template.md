# Course Project Proposal

**Team Members:** Core RL Course Project

**Working Direction / Title:** Off-Policy GVF Stability Under Behavior Drift

## What do you want to understand?

Whether background predictions learned from ordinary off-policy experience remain stable when the behavior policy drifts. The focused RL question is: which small linear TD corrections prevent GVF learning from becoming unstable under off-policy sampling, bootstrapping, and function approximation?

## What setting or testbed will you use?

Baird-style diagnostic chains and a small GVF/Horde-like sensor stream where target questions differ from the behavior policy and behavior probabilities change over time.

## What will you examine?

Off-policy TD, TDC/GTD-style gradient correction, emphatic TD, centered variants, and normalized/output-controlled variants. The study remains linear and streaming.

## What will you look at?

Weight norm, projected value error, MSPBE-style proxy, divergence rate, follow-on trace scale, and stability-region plots over behavior mismatch and alpha. A useful result identifies where background prediction is safe or unsafe.
