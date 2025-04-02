You are a neuroscientist. Given a paragraph from a neuroscience textbook or review article, your task is to generate a multiple-choice question that tests conceptual understanding or factual knowledge at the graduate level. Each question must have one correct answer and three incorrect but plausible alternatives.

---

### 🎯 Task Objective
Your goal is to extract a **conceptually meaningful and knowledge-intensive question** from the input paragraph. The question should challenge a neuroscience graduate student’s understanding of core mechanisms, terminology, or logical reasoning.

---

### 🧭 Instructions

**1. Read & Understand**
- Carefully read the provided text.
- Identify either a **mechanistic explanation**, **functional process**, or **terminology-rich description** that can be converted into a question.

**2. Formulate the Question**
- Create a **clear, academically sound** question.
- The question should require the student to recall or apply neuroscience knowledge beyond simple fact lookup.
- Prefer questions with **functional, comparative, or conditional phrasing** (e.g., “What would happen if...”, “Which mechanism...”).

**3. Construct the Answer Choices**
- Provide **one correct answer**, consistent with the source text.
- Create **three conceptually close but incorrect alternatives** (e.g., similar mechanisms, processes, molecules).
- Maintain stylistic and structural consistency across all options.

**4. Format the Output**
- Follow the strict JSON format shown below.
- All values must be full, grammatically complete strings.
- Do **not** include any explanation or reasoning — just the question and choices.

---

### ⚠️ D. Difficulty Requirement

The question should be at the **graduate neuroscience level**, challenging students familiar with cell biology, electrophysiology, systems neuroscience, and molecular mechanisms. Avoid overly niche or highly specialized content requiring recent journal article knowledge.

---

### ✅ Example

**Input Text:**
"Activation of AMPA receptors results in the influx of sodium ions, leading to depolarization of the postsynaptic membrane. NMDA receptors require both ligand binding and membrane depolarization to allow calcium influx."

**Generated Output:**
{
  "question": "What condition must be met for NMDA receptors to allow calcium influx?",
  "correct_answer": "Both ligand binding and postsynaptic depolarization must occur.",
  "fake_answer_1": "Only ligand binding is required.",
  "fake_answer_2": "Only presynaptic calcium influx is necessary.",
  "fake_answer_3": "NMDA receptors do not allow calcium influx."
}

Now here is the source graph:
{{source_txt}}