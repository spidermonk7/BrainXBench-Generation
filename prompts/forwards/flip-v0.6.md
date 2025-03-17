# **Abstract Modification Instructions**  

You will see the **Research Background**,  **Research Method** and **Conclusion** of a **neuroscience research paper**. You are tasked with **introducing subtle but critical errors** into the **Conclusion** sections. The change you made should make the conclusions incorrect while ensuring that the structure and readability of the abstract remain intact.

---

## **Modification Requirements**  

1. **Opposite Outcome**  
- **Identify and reverse one of the experimental results** in the conclusion section while keeping the structure of the sentence intact, **Attention**! You should only reverse **ONE** result.  
- If the study states **X increases Y**, modify it to **X decreases Y**.  
- If the study states **X has no effect on Y**, modify it to **X has a strong effect on Y**.  
- **Do not modify words that indicate experimental demonstration or statement**, such as *"demonstrate," "show," "indicate," "suggest,"* or *"provide evidence."* These words should remain unchanged to ensure the modification appears natural and does not alter the tone of the scientific claim.  

Ensures that only **the one core scientific findings are reversed**, while the language framing the conclusion remains consistent and natural. 


2. **Inverse Causality Modification**  
- Reverse the **causal claim** of **one key scientific conclusion** in the Conclusion section.  
- Ensure the reversal **targets the paper’s main claim**, not the experimental method, observed phenomena, or result interpretation.  
- Maintain academic tone and sentence structure while ensuring the reversed causality remains **plausible** in the neuroscience context.  
- **Causality should be modified within the research findings.** If the result states **“A increases, leading to B increasing,”** this should be reversed. However, if it states **“Based on experimental evidence A, we conclude B,”** this should **not** be changed, as it does not meet the criteria.  
- Do **not** simply negate the conclusion or introduce a different relationship—only invert the causal direction.

3. **Factor Misattribution Modification**  
Modify **one key scientific conclusion** in the Conclusion section by **replacing the explanatory factor (X) with a misleading but plausible confounding factor (Z).**  

- Identify the original causal factor **X** that explains the outcome **Y** and replace it with **Z**, ensuring **Z sounds scientifically reasonable** but is not the true cause.  
- **Leverage the Background and Method sections** to select the **most deceptive misattribution**—one that could plausibly mislead readers.  
- Keep the sentence structure intact while ensuring the claim remains **deceptively plausible** based on the paper’s **method and background.**  
- **Do not** reverse the result itself—if the original states **“X increases Y,”** the modification should still state **“Z increases Y,”** not that **Y decreases.**  
- Avoid obvious logical errors—**the incorrect factor should be misleading but not nonsensical.**

4. **Balderdash**
   - Modify the Conclusion, make it still seems like research result corresponding to the background but make no sense. But still, you should keep the words coherent and sound natural within the abstract.
---

### **Important Instructions:**  
1. **Each modification should be subtle but significantly alter the meaning of the original abstract, for each modification, you can only modify less than two sentences**  

2. **Ensure all modified sections remain coherent and sound natural within the abstract.**  
   - The errors should not appear forced, self-contradictory, or out of place in an academic setting.  

3. **Output must be in JSON format, and each value must contain the full section with the modified sentence naturally integrated.**  
   - **Do not return only the modified sentence—return the entire paragraph with the change embedded.**  

4. **Strict Output Format:**  
{   
    "Opposite_Outcome": "Full Conclusion section with the modified sentence naturally integrated.",
    "Incorrect_Causal_Relationship":  "Full Conclusion section with the modified sentence naturally integrated.", 
    "Factor_Misattribution": "Full Conclusion section with the modified sentence naturally integrated.", 
    "Balderdash": "Full Conclusion section with the modified sentence naturally integrated."
}
---
### **Original Research Background:**
{{background}}

### **Original Research Methods:**  
{{method}}  

### **Original Conclusion:**  
{{results}}  
