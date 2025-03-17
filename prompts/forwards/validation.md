### **Polished Prompt**  

---

### **Task: Validate the Modifications of a Neuroscience Research Conclusion**  

You are given the **initial Conclusion section** of the abstract from a neuroscience research paper, along with **three modified versions** that correspond to three specific modification types:  
- **Opposite Outcome**  
- **Factor Misattribution**  
- **Incorrect Causal Relationship (Inverse Causality)**  

Your task is to validate whether each modification meets the specified criteria.  

---

### **Modification Requirements**  

#### **1️⃣ Opposite Outcome**  
- **Reverse exactly ONE experimental result** while keeping the sentence structure intact.  
- If the original states **"X increases Y,"** modify it to **"X decreases Y."**  
- If the original states **"X has no effect on Y,"** modify it to **"X has a strong effect on Y."**  
- **Do not modify** words that indicate scientific demonstration, such as *"demonstrate," "show," "indicate," "suggest,"* or *"provide evidence."*  
- Ensure **only ONE** core scientific finding is reversed while keeping the overall framing and tone consistent.  

✅ **Valid Example:**  
- **Original:** "Dopamine release in the prefrontal cortex enhances cognitive flexibility."  
- **Modified:** "Dopamine release in the prefrontal cortex reduces cognitive flexibility."  

❌ **Invalid Example:**  
- **Modified:** "Dopamine release in the prefrontal cortex is unrelated to cognitive flexibility." (Introduces an alternative claim rather than reversing the outcome.)  

---

#### **2️⃣ Incorrect Causal Relationship (Inverse Causality)**  
- **Reverse the cause-and-effect relationship** in one key scientific conclusion while keeping the sentence structure intact.  
- Ensure the modification **targets the research findings,** not the experimental method, observed phenomena, or interpretation of results.  
- If the original states **“A increases, leading to B increasing,”** reverse it to **“B increases, leading to A increasing.”**  
- If the sentence states **"Based on experimental evidence A, we conclude B,"** **do not modify it**, as this does not reflect a causal claim.  

✅ **Valid Example:**  
- **Original:** "Neural synchrony in the hippocampus enhances memory retention."  
- **Modified:** "Memory retention enhances neural synchrony in the hippocampus."  

❌ **Invalid Example:**  
- **Modified:** "Neural synchrony in the hippocampus does not enhance memory retention." (Negates the claim rather than reversing causality.)  

---

#### **3️⃣ Factor Misattribution**  
- Replace the **true explanatory factor (X) with a misleading but scientifically plausible factor (Z)** while keeping the sentence structure intact.  
- **The new factor (Z) must be deceptively plausible** based on the **Background and Methods sections** but should **not** be the actual cause of the observed outcome.  
- **Do not reverse the result itself**—if the original states **“X increases Y,”** the modification should still state **“Z increases Y.”**  
- Avoid making the modification too obviously incorrect; **it should appear misleading yet scientifically reasonable.**  

✅ **Valid Example:**  
- **Original:** "Hippocampal theta oscillations regulate spatial memory retrieval."  
- **Modified:** "Cerebellar activity regulates spatial memory retrieval."  

❌ **Invalid Example:**  
- **Modified:** "Hippocampal theta oscillations regulate heart rate." (Introduces a completely unrelated claim instead of a misleading misattribution.)  

---

### **Validation Questions & JSON Output Format**  

For each modification, answer the following questions:  

#### **(1) Opposite Outcome**  
- **(1-1)** What is the exact modification?  
- **(1-2)** Does it meet the requirements? (1 = Yes, 0 = No)  

#### **(2) Factor Misattribution**  
- **(2-1)** What is the exact modification?  
- **(2-2)** Does it meet the requirements? (1 = Yes, 0 = No)  

#### **(3) Incorrect Causal Relationship**  
- **(3-1)** What is the exact modification?  
- **(3-2)** Does it meet the requirements? (1 = Yes, 0 = No)  

---

### **Response Format (JSON Output)**  

Your response should follow this JSON format:  

```json
{
    "Opposite_Outcome": {
        "modification": "modified sentence here",
        "valid": 1 or 0
    },
    "Factor_Misattribution": {
        "modification": "modified sentence here",
        "valid": 1 or 0
    },
    "Incorrect_Causal_Relationship": {
        "modification": "modified sentence here",
        "valid": 1 or 0
    }
}
```

---
Here are the inputs

## Initial Conclusion Section:  
{{initial_conclusion}}  

## Modified: Opposite Outcome  
{{Opposite_Outcome}}  

## Modified: Factor Misattribution  
{{Factor_Misattribution}}  

## Modified: Incorrect Causal Relationship  
{{Incorrect_Causal_Relationship}}  


