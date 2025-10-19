# 🧠 ReCAP: Recursive Context-Aware Reasoning and Planning

This repository contains the implementation and benchmark evaluations for **ReCAP (Recursive Context-Aware Reasoning and Planning)**, as described in our NeurIPS 2025 paper:

> **ReCAP: Recursive Context-Aware Reasoning and Planning for Large Language Model Agents**  
> *Zhenyu Zhang\*, Tianyi Chen\*, Weiran Xu\*, Alex Pentland, Jiaxin Pei*  
> (\*Equal contribution)  
<!-- > [Paper (NeurIPS 2025)](./NeurIPS_2025_RECAP_Camera_Ready.pdf) -->

---

## 📘 Overview

**ReCAP** is a hierarchical reasoning and planning framework for large language model (LLM) agents.  
It enables long-horizon, context-consistent reasoning by combining:

1. **Plan-ahead task decomposition** – generate a complete ordered subtask list, execute the head item, and refine the remainder.  
2. **Structured context re-injection** – maintain a single shared LLM context across recursive depths, preserving high-level intent.  
3. **Sliding-window scalability** – keep the prompt bounded while reintroducing essential plan context, enabling linear cost growth with task depth.

ReCAP achieves large performance gains over sequential and hierarchical baselines (e.g., ReAct, ADaPT) across long-horizon reasoning tasks such as **Robotouille**, **ALFWorld**, **FEVER**, and **SWE-bench Verified**.

---

## 🗂 Repository Structure

```
ReCAP-main/
│
├── alfworld-recap/
│   ├── README.md
│   ├── ...
│   # ReCAP implementation and experiments on the ALFWorld benchmark.
│   # Includes full evaluation code, prompts, and logging utilities for both
│   # ReCAP and baseline agents (e.g., ReAct, Act, CoT).
│
├── fever-recap/
│   ├── README.md
│   ├── ...
│   # ReCAP and baseline implementations on the FEVER fact verification benchmark.
│   # Contains prompt templates for search/lookup/finish reasoning loops and evaluation scripts.
│
├── swebench-verified-recap/
│   ├── README.md
│   ├── ...
│   # Full code for running ReCAP and baseline agents on the SWE-bench Verified dataset.
│   # Includes integration with the SWE-bench environment, JSON schema definitions,
│   # and GPT-4.1-compatible prompting logic.
│
├── robotouille-baseline/
│   ├── README.md
│   ├── ...
│   # Baseline agent implementations (ReAct, CoT, Act, Standard, ADaPT) for Robotouille.
│   # Reproduces results reported in Table 1 of the paper.
│
├── robotouille-recap/
│   ├── README.md
│   ├── ...
│   # Our ReCAP implementation for Robotouille (synchronous + asynchronous settings).
│   # Includes all task definitions, recipe setups, logging, and visualization scripts.
│
└── README.md
    # (This file)
```

---

## ⚙️ Setup

Each subdirectory contains its own `README.md` with setup and execution instructions.  
In general, experiments can be reproduced as follows:

```bash
cd robotouille-recap
pip install -r requirements.txt
python run_recap.py --env robotouille --mode async
```

All experiments use GPT-4o via the OpenAI API, unless otherwise specified.

---

## 🧩 Benchmarks Included

| Benchmark | Domain | Description | Evaluated Methods |
|------------|---------|--------------|-------------------|
| **Robotouille** | Embodied reasoning | Long-horizon cooking tasks (synchronous/asynchronous) | ReCAP, ADaPT, ReAct, CoT, Act |
| **ALFWorld** | Embodied reasoning | Text-based household environment | ReCAP, ReAct, Act |
| **FEVER** | Knowledge reasoning | Fact verification via Wikipedia API | ReCAP, ReAct, CoT, Act |
| **SWE-bench Verified** | Code reasoning | Repository-level issue resolution | ReCAP, ReAct (mini-SWE-agent baseline) |

---

## 🧪 Reproducibility

- All evaluations follow a strict pass@1 protocol (no retries, beam search, or self-consistency).  
- Each agent runs under identical API settings and budget constraints.  
- Environment rules, one-shot demonstrations, and prompt templates are included per benchmark directory.

---

## 📄 Citation

If you use this repository or ReCAP in your research, please cite:

```bibtex
@inproceedings{zhang2025recap,
  title     = {ReCAP: Recursive Context-Aware Reasoning and Planning for Large Language Model Agents},
  author    = {Zhenyu Zhang and Tianyi Chen and Weiran Xu and Alex Pentland and Jiaxin Pei},
  booktitle = {Conference on Neural Information Processing Systems (NeurIPS)},
  year      = {2025}
}
```
