You are an expert question generator. Your task is to extract a correct statement from a given text, modify it to create a plausible but incorrect statement, and present both as answer choices. Follow these instructions:

1. Carefully read the provided text.
2. Identify **some factual statement** from the text.
3. Modify it slightly to create {{question_num}} **plausible but incorrect** statement while keeping it grammatically correct.
4. Present both the **correct** and **incorrect** statements as answer choices (A and B).
5. Indicate which statement is correct.
6. Ensure the incorrect statement is subtle but still **clearly false**.
7. Output following a strict json format. 

### **Example:**
**Input Text:**
"Jupiter is the largest planet in the Solar System and has a strong magnetic field. It primarily consists of hydrogen and helium."

**Generated Question:**

{
    "Q1": {
        "Description A": "Jupiter is the largest planet in the Solar System and has a strong magnetic field.",
        "Judge A": "True",
        "Description B": "Jupiter is the smallest planet in the Solar System and has a weak magnetic field."
        "Judge B": "False",
        "Answer": "Description A"
    },
    "Q2": {
        "Description A": "Jupiter primarily consists of hydrogen and oxygen.",
        "Judge A": "False",
        "Description B": "Jupiter primarily consists of hydrogen and helium. "
        "Judge B": "True",
        "Answer": "Description B"
    }
}

Now, generate a correct and incorrect statement for the following text:
{{source_txt}}
