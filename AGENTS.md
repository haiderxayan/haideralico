# Agent Preferences for This Repo

These instructions apply to agent sessions working in this repository.

## Model Selection
- Default model: `gpt-5-codex low`.
- Fallback model: `gpt-5-codex minimal` when encountering usage/rate limits (e.g., 429 or “usage limit reached”).

## Usage Guidance
- Prefer concise outputs and minimal context windows to conserve tokens.
- If a request requires heavier reasoning temporarily, step up one tier for that turn only, then return to the default.

## Scope
- This file’s scope is the entire repository.

