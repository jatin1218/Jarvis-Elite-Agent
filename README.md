
# JARVIS ELITE

## Multi-Agent Voice Assistant for Real-World Task Automation & Conversational AI

### Capstone Project – Kaggle Submission

**Author:**
Jitendra Vishwakarma 

---

## 1. Abstract

**JARVIS ELITE** is a production-oriented **multi-agent voice assistant platform** that integrates **large language models (LLMs)** with **real-time speech recognition**, **desktop automation tools**, **persistent memory systems**, and **observability pipelines**.

Unlike traditional single-agent assistants, JARVIS ELITE adopts a **parallel multi-agent architecture** where:

* Task execution (tool automation) and
* Conversational reasoning (LLM inference)

operate simultaneously, drastically reducing latency and enabling sophisticated real-world control flows.

This project demonstrates advanced **agent orchestration**, practical LLM tool-use, system telemetry, persistent contextual memory, automated evaluation, and REST API deployment — fulfilling all required competencies for the Kaggle capstone program.

---

---

## 2. Problem Statement

Modern voice assistants and chatbots typically rely on **monolithic agent architectures** that exhibit several limitations:

1. **Sequential bottlenecks** — LLM instruction processing and tool execution cannot occur concurrently.
2. **Lack of personalization** — Session memory is either nonexistent or unstructured.
3. **No agent observability** — Debugging and performance measurement are impractical.
4. **Limited extensibility** — Adding new skills requires modifying tightly-coupled core logic.
5. **Poor production readiness** — Minimal testing pipelines and no reliability metrics.

---

### Objective

Design and implement a **scalable, modular multi-agent assistant framework** that:

* Enables **parallel reasoning and execution**
* Maintains **persistent contextual memory**
* Supports **real-time speech interaction**
* Is instrumented with **observability and evaluation tools**
* Provides extensible APIs for future development

---

---

## 3. Solution Overview

JARVIS ELITE fulfills these objectives using a **coordinated multi-agent system** where:

### Principal Agents

| Agent                       | Function                                           |
| --------------------------- | -------------------------------------------------- |
| **Planner Agent**           | Classifies user intent and routes commands         |
| **Executor Agent**          | Executes local/system automation tasks             |
| **Conversation Agent (AI)** | Processes LLM reasoning using Gemini               |
| **Memory Agent**            | Stores & retrieves conversation history (Supabase) |
| **Observability Agent**     | Captures logs and runtime metrics                  |

---

### Agent Coordination Model

User input is first evaluated by the **Planner Agent**.

* **Executor Commands:**
  → Executor and AI agents run **in parallel**, providing immediate system action with simultaneous conversational acknowledgment.

* **Conversation Queries:**
  → Routed **sequentially** to the AI Agent with memory-augmented prompts.

---

### Parallel Execution Architecture

```text
User Input
    ↓
Planner Agent
    ↓
 ┌───────────────┐
 │               │
Executor Agent   AI Agent
 │               │
System Action ← Natural Language Response
```

This ensures:

* Reduced response latency
* Multi-modal feedback
* Separation of concerns

---

---

## 4. System Capabilities

### Voice Automation Modules

| Mode                          | Functional Scope                                     |
| ----------------------------- | ---------------------------------------------------- |
| **Google Mode**               | Voice-controlled search, scrolling, navigation       |
| **YouTube Mode**              | Media playback controls (play/pause/skip/fullscreen) |
| **WhatsApp Mode** *(Windows)* | App launch, contact lookup, message dictation        |
| **General Assistant**         | Open-domain Q&A via Gemini LLM                       |

---

### Core Technical Features

* **Speech Recognition:** Google STT
* **Text-to-Speech:** Windows SAPI voice synthesis
* **Desktop Control:** PyAutoGUI automation layer
* **Persistent Memory:** Supabase-backed conversation logs
* **Context Engineering:** Conversation summarization pipelines
* **Observability:** Agent-level logs and metrics
* **Evaluation:** Automated LLM output benchmarking
* **Deployment:** FastAPI microservice with REST endpoints

---

---

## 5. System Architecture

### Functional Flow

```text
Microphone Input
      ↓
Speech Recognition
      ↓
Planner Agent
      ↓
Intent Classification
      ↓
 ┌─────────────────────────────────────┐
 │                                     │
Executor Agent → System Automation     AI Agent → LLM Reasoning
 │                                     │
 └─────────────── Parallel Run ─────────┘
                    ↓
               Voice Output / API Response
                    ↓
        Memory Persistence & Observability
```

---

### Project Structure

```text
├── agents.py               # Multi-agent orchestration
├── context_engineering.py  # History summarization logic
├── database.py             # Supabase connectivity
├── memory.py               # Persistent memory agent
├── observability.py        # Logging and telemetry
├── evaluation.py           # LLM accuracy benchmarks
├── main.py                 # FastAPI server + voice loop
├── test_agents.py          # Integration test harness
└── requirements.txt
```

---

---

## 6. Course Objectives Mapping

This project directly implements all required Kaggle program competencies:

| Course Topic              | Implementation                              |
| ------------------------- | ------------------------------------------- |
| **LLM Agents**            | Gemini-powered conversational agent         |
| **Parallel Agents**       | Concurrent executor + AI acknowledgment     |
| **Sequential Agents**     | Planner → AI dialog workflows               |
| **Tool Systems**          | PyAutoGUI, SpeechRecognition, OS automation |
| **OpenAPI Tools**         | FastAPI REST services                       |
| **Long-running Sessions** | Supabase memory storage                     |
| **Context Engineering**   | History summarization pre-prompts           |
| **Evaluation**            | Automated benchmarking suite                |
| **Observability**         | Structured logging & metrics tracking       |

---

---

## 7. Installation

### Requirements

* Python 3.10+
* Windows OS (voice automation + WhatsApp module)
* Google Gemini API Key
* Supabase Account *(optional)*

---

### Setup

```bash
git clone <YOUR_GITHUB_REPO>
cd jarvis-elite-agent
pip install -r requirements.txt
```

Create `.env` file:

```env
GOOGLE_API_KEY=your_gemini_api_key

SUPABASE_URL=your_supabase_url   # optional
SUPABASE_KEY=your_supabase_key  # optional
```

---

---

## 8. Running the Project

### Start Voice Assistant

```bash
python main.py
```

**Wake Words:**

```
"Hey Jarvis" | "OK Jarvis"
```

**Exit Command:**

```
"exit"
```

---

### Run API Server

```bash
uvicorn main:app --reload
```

#### API Endpoints

| Endpoint    | Description                      |
| ----------- | -------------------------------- |
| `/`         | Service heartbeat                |
| `/ask`      | Submit LLM or tool-based queries |
| `/evaluate` | Run benchmark evaluation         |
| `/health`   | Platform capability report       |

---

---

## 9. Evaluation

Automated accuracy testing is implemented in `evaluation.py`.

Run:

```bash
python -c "from evaluation import run_evaluation; print(run_evaluation())"
```

### Sample Output

```json
{
  "accuracy": "100%",
  "tests_passed": 3,
  "tests_total": 3
}
```

This verifies:

* Reliable communication with Gemini API
* Agent routing correctness
* Content relevance matching

---

---

## 10. Real-World Applications

* Personal desktop assistant
* Productivity automation
* Accessibility support
* Educational tutoring systems
* Robotics control frameworks
* Multimodal smart-home hubs

---

---

## 11. Limitations

* Desktop automation currently optimized for **Windows OS**
* WhatsApp integration requires desktop app focus
* Gemini API rate limits depend on free-tier quotas
* Speech recognition depends on audio quality

---

---

## 12. Future Enhancements

* Vision-based control modules (camera input)
* Autonomous task chaining workflows
* Additional LLM provider support (OpenAI / Anthropic / Azure)
* Android/iOS mobile integration
* Reinforcement learning for action optimization
* Neural speech synthesis upgrade

---

---

## 13. Ethical Use

This project is developed strictly for:

* Educational
* Research
* Responsible experimentation

Users must ensure compliance with:

* Platform ToS (WhatsApp, YouTube, Google)
* Privacy laws regarding voice data capture

No sensitive data is stored without explicit user consent.

---

---

## 14. License

MIT License — Open for academic and non-commercial use.

---

---

## ⭐ Kaggle Capstone Highlights

✅ Full **multi-agent orchestration system**
✅ Parallel execution methodology
✅ Practical desktop automation tools
✅ Memory persistence with database storage
✅ Evaluation and telemetry instrumentation
✅ RESTful LLM deployment
✅ Real-world voice assistant capability

---

---

## Acknowledgments

* **Google Gemini API**
* **FastAPI**
* **Supabase**
* **SpeechRecognition**
* **PyAutoGUI**

