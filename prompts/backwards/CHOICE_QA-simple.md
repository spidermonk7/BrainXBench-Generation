### 🎯 Task Objective
Your goal is to extract a **fact-based question** from the input paragraph that tests basic neuroscience knowledge. The question must be directly answerable based on the provided text.

---

### 🧭 Instructions

**1. Read & Understand**
- Carefully read the provided text.
- Identify a **factual statement** or well-defined concept suitable for a question.

**2. Formulate the Question**
- Write a **concise, clear, and specific** question based on the chosen fact.
- Avoid ambiguous, open-ended, or opinion-based phrasing.

**3. Construct the Answer Choices**
- Provide **one correct answer**, supported directly by the text.
- Generate **three incorrect but plausible distractors**, ideally related in topic or category.
- Keep all answer choices consistent in tone and length.

**4. Format the Output**
- Output should follow the **strict JSON format** below.
- Each value must be a **complete string** (no nulls or partial phrases).
- Do **not** include explanations or reasoning—just the question and choices.

---

### ⚠️ D. Difficulty Requirement

The question should be **simple and accessible**, such that a **well-educated high school student** could understand and answer it correctly. Avoid highly specialized terminology or graduate-level detail.

---

### ✅ Example

**Input Text:**
"The myelin sheath is a fatty layer that wraps around the axons of some neurons. It helps increase the speed at which electrical impulses travel along the nerve cell."

**Generated Output:**
{
  "question": "What is the function of the myelin sheath in neurons?",
  "correct_answer": "It increases the speed of electrical impulse conduction.",
  "fake_answer_1": "It stores neurotransmitters for later release.",
  "fake_answer_2": "It generates action potentials in the axon hillock.",
  "fake_answer_3": "It blocks signals from reaching the synapse."
}

Now here is the paragraph:
{{source_txt}}