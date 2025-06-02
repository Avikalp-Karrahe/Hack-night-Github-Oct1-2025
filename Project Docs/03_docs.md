# GitRead – Agent Behavior Reference

## Runtime Behavior

When GitRead is invoked, it will:

1. **Clone** the target GitHub repo
2. **Parse** its README, structure, and dependencies
3. **Build a project document** using a chain-of-thought strategy:
   - Prompt 1: Generate high-level outline
   - Prompt 2-N: Fill sections (overview, usage, modules, APIs, envs, etc.)
4. **Read user’s prior knowledge** from:
   - `ai_learning/` (for summaries, prompt strategy, explanation style)
   - `project_docs/gitread/` (for iterations, change history)

## Prompt Templates (Meta-Prompting Style)
\`\`\`text
You are a senior technical writer. Given this parsed repository and relevant user knowledge, generate a markdown project doc including:
- Overview
- Tech Stack
- Installation Steps
- Key Modules & Files
- API Endpoints
- Environment Variables
- Testing Strategy
\`\`\`

## Expected Outputs
- `project_doc.md`
- Optionally: `.pdf` and `.html` using pandoc

## Agent Memory Rules
- Use `ai_learning/` to enhance reasoning
- Compare current results with previous versions in `project_docs/gitread/`
- Self-improve on next run
