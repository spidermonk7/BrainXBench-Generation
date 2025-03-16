# **Abstract Modification Instructions**  

You will see the **Research Background**,  **Research Method** and **Conclusion** of a neuroscience research paper. You are tasked with modifying an abstract by **introducing subtle but critical errors** into the **Conclusion** sections. These changes should make the conclusions incorrect while ensuring that the structure and readability of the abstract remain intact.
## **Modification Requirements**  

---
1. **Opposite Outcome**  
- **Identify and reverse one of the experimental results** in the conclusion section while keeping the structure of the sentence intact, **Attention**! You should only reverse **ONE** result.  
- If the study states **X increases Y**, modify it to **X decreases Y**.  
- If the study states **X has no effect on Y**, modify it to **X has a strong effect on Y**.  
- **Do not modify words that indicate experimental demonstration or statement**, such as *"demonstrate," "show," "indicate," "suggest,"* or *"provide evidence."* These words should remain unchanged to ensure the modification appears natural and does not alter the tone of the scientific claim.  

Ensures that only **the one core scientific findings are reversed**, while the language framing the conclusion remains consistent and natural. 

2. **Inverse Causality**
   - Reverse the Causality of the original conclusion. 
   - If the study states **X leads to Y**, modify it to **Y leads to X**. 

- Modify the Conclusion section by reversing the cause-and-effect relationship while keeping the sentence structure intact. This means swapping the roles of the dependent and independent variables to create a misleading conclusion.
1) Identify the causal relationship in the original conclusion:
Original: "X causes Y."
Modified: "Y causes X."
2) Ensure that the reversed relationship still sounds reasonable in the context of neuroscience research, even though it is incorrect.
3) Do NOT change the wording unnecessarily—only reverse the causal flow while maintaining the academic tone.
4) Avoid creating a sentence where the reversed causality makes no sense.
**Examples**
✅ Valid Modification (Causal Reversal)
- Original: "Dopamine release in the prefrontal cortex regulates decision-making speed."
- Modified: "Decision-making speed regulates dopamine release in the prefrontal cortex." (This reverses the causality but remains a plausible claim.)
- Original: "Neural synchrony in the hippocampus enhances memory retention."
- Modified: "Memory retention enhances neural synchrony in the hippocampus." (Sounds possible but is factually incorrect.)

❌ Invalid Modification (Logical Error or Incorrect Approach)
- Modified: "Neural synchrony in the hippocampus does not enhance memory retention." (This is negating the relationship, not reversing it.)
- Modified: "Neural synchrony in the hippocampus enhances heart rate regulation." (This is introducing a different relationship, not reversing causality.)
Edge Cases to Consider:

**Double Negation Avoidance:**
If the original sentence contains a negation (e.g., "X does not cause Y."), reversing the relationship should not create another negation that neutralizes the change.
Example:
- Original: "Cortical activation does not influence motor learning."
Incorrect Modification: "Motor learning does not influence cortical activation." (This is just flipping words, not reversing causality.)
- Correct Modification: "Motor learning influences cortical activation."


3. **Factor Misattribution**
Modify the Conclusion section by introducing a confounding factor misattribution, which means replacing the original key explanatory variable with an incorrect one. The new factor must still sound scientifically plausible within the neuroscience domain but should not be the actual cause of the observed results.

1) Identify the key factor (X) that is stated to influence the outcome (Y) in the original conclusion.
Replace X with a scientifically plausible but incorrect factor (Z), while keeping the structure of the sentence intact.
2) Ensure that Z is somewhat related to the research context but does not logically explain Y.
Do NOT reverse the result itself (i.e., if the conclusion states that X increases Y, your modification should still state that Z increases Y, rather than decreasing Y).
3) Avoid making obvious logical errors—the modified conclusion should still read naturally and appear valid at first glance.
**Examples**
✅ Valid Modification (Incorrect Confounding Factor)
- Original: "Hippocampal theta oscillations regulate spatial memory retrieval."
- Modified: "Cerebellar activity regulates spatial memory retrieval." (The cerebellum is involved in motor coordination, not directly in memory retrieval.)
- Original: "Cortical dopamine levels modulate cognitive flexibility."
- Modified: "Serotonin levels modulate cognitive flexibility." (Serotonin affects mood and emotion but is not the primary neuromodulator for cognitive flexibility.)

❌ Invalid Modification (Logical Error or Incorrect Approach)
- Modified: "Hippocampal theta oscillations do not regulate spatial memory retrieval." (This is reversing the result, not introducing a confounding factor.)
- Modified: "Hippocampal theta oscillations regulate heart rate." (This creates an illogical relationship rather than an incorrect but plausible confounding factor.)


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
    "Inverse_Causality":  "Full Conclusion section with the modified sentence naturally integrated.", 
    "Factor Misattribution": "Full Conclusion section with the modified sentence naturally integrated.", 
    "Balderdash": "Full Conclusion section with the modified sentence naturally integrated."
}
---
### **Original Research Background:**
{{background}}

### **Original Research Methods:**  
{{method}}  

### **Original Conclusion:**  
{{results}}  
