# GitRead – Agent Blueprint

## 🔍 Agent Purpose
GitRead is an AI agent that reads any public GitHub repository and outputs a structured project document.

Unlike a static script, GitRead is part of a **self-evolving agent ecosystem**. It improves by accessing two persistent memory sources:

- 📚 `ai_learning/` – What I’ve learned about AI and agent design
- 📁 `project_docs/gitread/` – This very plan, its past docs, iterations, and outputs

## 🧠 Core Design Principles (from DX Guide)
- **Unit Work**: Break tasks into composable chunks (e.g., "summarize one file")
- **Prompt Chaining**: Outline → Section Details → Final Doc
- **Meta-Prompting**: Frame the LLM role with identity ("You're a documentation engineer")
- **Self-Correction**: Review its own output, compare with past runs
- **Tool Use**: Use real engineering tools (`git`, `tree-sitter`, `pandoc`, etc.)
- **User Alignment**: If in doubt, ask or fallback to my `ai_learning` knowledge base

## 🔄 Input Contexts
- Active GitHub repo (cloned)
- Indexed notes from `ai_learning/`
- This folder's plan, past docs, and changelogs

## ✅ MVP Steps
1. Clone repo
2. Parse code, README, dependencies
3. Chain prompts to generate `project_doc.md`
4. Query `ai_learning` for enhancement
