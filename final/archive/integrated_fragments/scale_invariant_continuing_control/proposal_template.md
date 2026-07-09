# Course Project Proposal

**Team Members:** Core RL Course Project

**Working Direction / Title:** Scale-Invariant Continuing Control: Reward and Feature Units in Streaming Sarsa

## What do you want to understand?

Whether a continuing control agent can remain behaviorally stable when two arbitrary units of the problem change: the reward origin and the feature scale. The focused RL question is: can reward-centered objectives and output-controlled updates jointly create invariance to reward translation and representation scaling in an online Sarsa agent?

## What setting or testbed will you use?

A continuing access-control queue and a continuing tile-coded grid/queue variant. The agent acts indefinitely, receives shifted rewards, and uses linear action values with scaled or uneven tile features.

## What will you examine?

Ordinary discounted Sarsa, reward-centered Sarsa, differential Sarsa, normalized reward-centered Sarsa, and trace-normalized variants. The experiment varies reward shift, feature scale, discount factor, and step-size.

## What will you look at?

Unshifted reward, Q norm, TD-error scale, prediction/action-value change per update, divergence, policy invariance, and recovery after reward/scale changes. The key figure is a two-dimensional invariance atlas over reward shift and feature scale.
