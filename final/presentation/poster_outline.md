# Poster Outline

## Title

Small Streaming RL Studies Through the Alberta Plan Lens

## Opening Question

How do simple online RL mechanisms behave when an agent must learn continually from a single experience stream, without replay buffers or deep networks?

## Main Panels

1. Alberta Plan framing
   - Ordinary experience.
   - Temporal uniformity.
   - Value functions, representation, planning, options.

2. Reward-centered continuing control
   - RL question: Does centering remove reward-shift sensitivity?
   - Show unshifted average reward and Q norm across reward shifts.

3. Output-controlled streaming prediction
   - RL question: Should step-size control parameter change or prediction change?
   - Show RMSE / divergence under feature scale changes.

4. Predictive state and feature utility
   - GVFs in T-maze.
   - Generate-and-test traces under delay shift.

5. Reusable structure
   - Doorway options in Four Rooms.
   - Dyna planning budget.

6. Reproducibility
   - Exact commands.
   - Seed list.
   - Result paths.
   - No replay, no deep networks.

## Takeaway

Small online experiments can expose Alberta Plan mechanisms directly: reward baselines, output-scale updates, predictive state, feature utility, temporal abstraction, and planning budget all matter before large-scale engineering enters the picture.
