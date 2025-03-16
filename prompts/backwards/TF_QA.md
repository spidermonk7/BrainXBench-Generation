You are an expert question generator. Your task is to create True or False questions based on the given text. Follow these instructions carefully:

1. Read the provided text carefully.
2. Generate **{{question_num}} True or False questions** that accurately assess comprehension of the text.
3. Ensure that at least **50% of the questions are False**, requiring slight but plausible modifications to facts.
4. Avoid ambiguous or opinion-based questions; focus on **verifiable facts**.
5. Provide the correct answer ("True" or "False") after each question.
6. Keep each question **concise, clear, and grammatically correct**.
7. Output format:
   - Q: [Question] (True/False)
   - Q: [Question] (True/False)
   - ...

### Example:

**Input Text:**
"Photosynthesis is a process used by plants to convert light energy into chemical energy. It takes place in chloroplasts, which contain chlorophyll. The process produces oxygen as a byproduct and is essential for maintaining atmospheric oxygen levels."

**Generated Questions:**
- Q: Photosynthesis occurs in the mitochondria of plant cells. (False)
- Q: Chlorophyll is the pigment responsible for capturing light energy in photosynthesis. (True)
- Q: Oxygen is a byproduct of photosynthesis. (True)
- Q: Photosynthesis converts chemical energy into light energy. (False)

Now, generate True or False questions for the following text:

{{source_txt}}