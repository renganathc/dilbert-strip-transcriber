# 📘 Dilbert Vision-Language Model Benchmark

A fully reproducible and deterministic benchmark evaluating Vision-Language Models (VLMs) on structured dilbert comic strip transcription with strictly defined evaluation rules.

### 🔗 **Live Demo:**
## https://renganathc.github.io/dilbert-strip-transcriber/

------------------------------------------------------------------------

## 🧠 Project Overview

This project benchmarks multiple open and closed Vision-Language Models
on the task of:

> Structured, panel-wise transcription of Dilbert comic strips (1990
> dataset)

Each model is evaluated on:

-   Text accuracy
-   Speaker identification
-   Panel structure
-   Hallucination control

All models are tested under identical prompting conditions to ensure
deterministic comparison.

------------------------------------------------------------------------

## ⚙️ Experimental Design

### 🔹 Generation Protocol

-   Identical **system prompt** and **user prompt** used for all models\
-   No per-model prompt tuning\
-   Ensures performance reflects model capability, not prompt
    engineering

------------------------------------------------------------------------

### 🔹 Evaluation Protocol

-   Parent judge model: **GPT-4o-mini**
-   Compared against manually transcribed ground truth
-   Deterministic scoring using strict weighted metrics

### Evaluation Weights

  Metric             |Weight
  ------------------ |--------
  Word Accuracy      |40
  Speaker Accuracy   |25
  Panel Structure    |20
  Hallucination      |15

-   Hallucinations penalized strictly\
-   No rewriting or inference allowed\
-   Scores computed using explicit mathematical aggregation

------------------------------------------------------------------------

## 📊 Dashboard Features

### 1️⃣ Overall Model Statistics

-   Average score across all 30 strips
-   Metric-wise breakdown
-   Fully sortable
-   D3 heatmap visualization

### 2️⃣ Per-Strip Leaderboard

-   Strip-wise comparison across all models
-   Row average calculation
-   Heatmap-normalized score visualization
-   Detailed modal view per strip

### 3️⃣ Per-Model Breakdown

-   Panel-level metric breakdown
-   First 5 rows visible by default
-   Expandable to full 30 strips
-   Fully normalized metric visualization

### 4️⃣ Strip Detail Viewer

Click **Details** to open:

-   Left → Original strip image
-   Right → Model outputs panel-by-panel
-   Side-by-side transcript comparison

------------------------------------------------------------------------

## 📂 Repository Structure

    dilbert-strip-transcriber/
    │
    ├── index.html
    ├── script.js
    │
    ├── evaluation_results/
    │   ├── gemini2.5_flash_lite2.json
    │   ├── gemma3_12b.json
    │   └── ...
    │
    ├── *_direct.json (raw model outputs)
    │
    ├── dilbert_1989_to_2023/
    │   └── 1990/
    │       ├── 1990-01-01_....gif
    │       └── ...

------------------------------------------------------------------------

## 🧪 Models Evaluated

-   Qwen 3 32B
-   Gemini 2.5 Flash Lite
-   LLaMA 4 Maverick
-   NVIDIA Nemotron 12B
-   LLaMA 3.2 11B
-   Gemma 3 12B
-   InternVL

(All evaluated under identical prompts.)

------------------------------------------------------------------------

## 🚀 Hosting

Hosted via **GitHub Pages** using static HTML, Bootstrap 5, and D3.js.

No backend required.

------------------------------------------------------------------------

## 🛠 Tech Stack

-   HTML5
-   Bootstrap 5
-   D3.js
-   Vanilla JavaScript
-   GitHub Pages

------------------------------------------------------------------------

## 🎯 Key Principles

-   Determinism
-   Transparency
-   Strict scoring
-   No hidden heuristics
-   Reproducibility

------------------------------------------------------------------------

## 📈 Why This Matters

Most VLM comparisons:

-   Use informal prompts
-   Use subjective evaluation
-   Do not penalize hallucinations strictly

This benchmark enforces:

-   Structured JSON outputs
-   Weighted deterministic scoring
-   Explicit hallucination penalties
-   Fixed evaluation rules


------------------------------------------------------------------------

## 📌 Future Extensions

-   Expand dataset beyond 1990
-   Convert to full benchmark paper
