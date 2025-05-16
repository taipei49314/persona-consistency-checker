# Persona Consistency Checker

A lightweight NLP module to verify consistency across user interactions based on a predefined persona.

## Features

- Analyze dialogue to detect semantic drift
- Score alignment with base persona traits
- Provide inconsistency reports for introspective feedback

## Directory Structure

- `data/` - Base persona and test dialogue data
- `src/` - Core logic for checking and utility functions
- `reports/` - Output reports from each analysis run
- `configs/` - Configuration settings

## How to Use

```bash
python src/consistency_checker.py --persona data/base_persona.json --dialogue data/test_dialogues.json
```

## License

MIT
