# Analysis: direct prompting, Chain-of-Thought, and ReAct

## Scenario

This assessment uses a campus equipment-rental desk. The private daily catalogue contains the rates for a camera, drone, and microphone. A user may ask a reasoning-only question, such as how many student sessions occur when computers are used in two shifts, or an information-dependent question, such as the discounted cost of renting equipment. The latter is deliberately not answerable reliably from a model's training data: the rates are private facts exposed only through `get_daily_rate`. The `calculator` tool performs arithmetic after the rates are retrieved.

## Explanation of the approaches

Direct prompting sends the question to the model with an instruction to return only a final answer. It is useful for simple, familiar questions and gives a fast, compact response, but it does not expose intermediate reasoning and has no tool access in this project. On a multi-step arithmetic question it may reach the correct result, but a reader cannot inspect the calculation. On the equipment-price question it cannot know the private rates and may produce a plausible but unsupported price. Its limitation in this scenario is therefore both hidden reasoning and unreliable access to current/private facts.

Chain-of-Thought (CoT) prompting asks the model to number the steps, show calculations, and finish with a `Final Answer:` line. This makes multi-step tasks such as applying a discount easier to audit and generally more reliable than direct prompting because the quantities and operations are explicit. CoT still uses only the information in the prompt and the model's learned knowledge: it cannot discover the private rate of a CAMERA or DRONE. Thus it improves reasoning over supplied facts but does not solve the information-retrieval limitation.

The ReAct agent alternates between deciding what it needs, taking an action, reading the observation, and continuing until it can answer. In `agent.py`, a rate question causes the model to call `get_daily_rate`; its result is placed back into the conversation as an observation. The agent then calls `calculator` for arithmetic and uses the result in its final response. This makes the price answer grounded in the catalogue and gives a visible action/observation trace. ReAct is not unlimited: it depends on correct tool choice, valid tool arguments, trustworthy tool data, and a step limit. It is also slower because each action usually needs another model request.

## Comparison

| Basis for comparison | Direct prompting | Chain-of-Thought | ReAct agent |
| --- | --- | --- | --- |
| Reasoning depth | Implicit and not shown | Explicit, ordered intermediate steps | Iterative reasoning tied to observations |
| Tool usage | None | None in this comparison | Calls rate lookup and calculator when needed |
| Reliability on multi-step questions | Can fail silently | Better when all facts are supplied | Best here when both calculation and private facts are needed |
| Transparency | Final answer only | Calculation is visible | Actions, observations, and final answer are visible |
| Speed / cost | Lowest: one short response | One response, often longer | Highest: one or more model calls plus tools |
| Consistency across repeated runs | Usually stable at temperature 0 | Stable at temperature 0; variation increases above 0 | Stable for deterministic tools, but model tool selection can vary |

## Self-consistency observation

`self_consistency.py` runs the first CoT question five times at temperature 0.8, extracts each `Final Answer:` line, and chooses the most common result. The expected calculation is `(1200 + 350) × 2 × 0.9 = 2790`, so the correct final answer is **Rs. 2,790**. After running the script with the selected provider, record its five printed answers in the submission screenshot; the script itself prints the observed majority and its count. If a minority response differs only in formatting, it should be normalised before interpreting it as mathematical disagreement. At temperature 0, the same prompt and provider normally give the same answer repeatedly, whereas a non-zero temperature intentionally allows alternative reasoning paths and makes majority voting useful.

## Suitability analysis

For this scenario, ReAct is the most suitable approach for price questions because it combines the two things the task needs: multi-step calculation and retrieval of private facts. The trace lets a reviewer verify each rate before accepting the final discount calculation. CoT is the better lighter-weight choice when all numbers are already in the question, because it is quicker and its steps are inspectable without the overhead of tools. Direct prompting is appropriate only when a concise answer is sufficient and the question does not require private/current information or an audit trail.

## Conclusion

Direct prompting is most appropriate for low-risk, straightforward requests where speed and a concise response matter more than an explanation. Chain-of-Thought is appropriate for problems whose relevant facts are already available and whose multi-step reasoning should be checked, such as arithmetic, ordering, or planning with supplied constraints. A ReAct agent is appropriate when solving the problem requires interacting with reliable external systems: databases, APIs, documents, calculators, or other tools. Its additional time and complexity are justified when the answer must be grounded in information the model cannot safely know by itself.
