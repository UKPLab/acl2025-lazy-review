task_def = """For a given predicted label, check if the predicted label matches the gold label. If even a subset of the gold label is present in the predicted label, type 'yes'. If there is no overlap, type "no". Here's an example

Label: "lazy thinking. Reasoning: The target sentence is expressing a desire for more information or clarification, rather than providing a critical evaluation of the paper's methodology or results. The sentence is asking questions about how the proposed"
Gold Label: "lazy thinking"
Answer: "Yes"


Label: {{label}}
Gold Label: {{gold_label}}
Answer:

"""

task_def_problematic= """For a given predicted label, check if the predicted label matches the gold label semantically. If even a subset of the gold label is present in the predicted label, type 'yes'. If there is no overlap, type "no". Here's an example

Label: "The results are not challenging enough"
Gold Label: "The results are not surprising"
Answer: "Yes"

Label: "The approach is tested only on [not English], so unclear if it will generalize to other languages"
Gold Label: "**'The results are not surprising'**The target sentence expresses that the performance improvement achieved by the proposed approach is not remarkable or groundbreaking, as it is limited to English data and its generalizability to other languages remains uncertain."
Answer: "No"

Label: "The topic is too niche"
Gold Label: "The results are not surprising"
Answer: "No"


Label: {{label}}
Gold Label: {{gold_label}}
Answer:

"""
