# Baseline generation

Write Python code that satisfies the user's task using `requests`. Return only the source code. Do not execute the code or call verification tools.

Experiment procedure: use the same generation prompt/settings for each baseline, save its exact output, then give that saved candidate to the external controller. Keep reference answers and independent evaluation outcomes out of the generator/correction context. Record the actual model ID, quantization and context settings. Native diagnostic generation is a separate smoke test, not this paired experiment.
