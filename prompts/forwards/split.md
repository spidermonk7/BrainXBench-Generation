You will be provided with an abstract of a research paper from {{subject}}. Your task is to **split** the abstract into three parts:

1) **Background** – The part of the abstract that explains the context or motivation for the research. Be sure to capture all context-related sentences without omissions.
2) **Method** – The part of the abstract describing the research methods, techniques, or approaches used in the study. Ensure this includes all relevant methods and approaches described in the abstract.
3) **Result** – The part of the abstract summarizing the findings or conclusions of the study. Extract every result-oriented sentence without leaving out any part of the findings or conclusions.

**Important: Make sure that the sum of the Background, Method, and Result exactly equals the original abstract. Each section should be extracted in full, and none of the content should be left out or altered. Your output should match the structure and content of the abstract.**

What's more, you also should: 
4) **If intact** - Since the abstracts are download from website, there could be some error leading to an incomplete download, judge if the abstract you got is intact! If it is, answer 1, otherwise 0. 
5) **Neuroscience related** - Please check if the abstract is Neuroscience related, if so, answer 1, otherwise 0. 
6) **Research_or_not** - Please check if its an research paper, if so, answer 1, otherwise 0, overview paper and perspective papers are out of our consideration. 

**You answer should be a json dict, which strictly follow the following format:**
{
    "Background": "those exact background sentences from the abstract",
    "Method": "those exact method sentences from the abstract",
    "Result": "those exact result sentences from the abstract", 
    "Intact_or_not": 1 or 0,
    "Neuroscience related": 1 or 0, 
    "Research_or_not": 1 or 0,
}
The abstract you need to process is as follows:
{{abstract}}

