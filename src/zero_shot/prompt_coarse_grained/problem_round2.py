round2_prompt_problematic = ''' As the number of scientific publications grows over the years, the need for efficient quality control in peer-reviewing 
becomes crucial. Due to the high reviewing load, the reviewers are often prone to different kinds of bias, which inherently contribute to 
lower reviewing quality and this overall hampers the scientific progress in the field. The ACL peer reviewing guidelines characterize some 
of such reviewing bias.  These are termed lazy thinking. The lazy thinking classes, their meaning and the reason for them being problematic 
are provided as a dictionary in the format ```key: meaning: reason for being problematic```. If a meaning or reason for being problematic is not known,
'' is provided in that place: 


{'The results are not surprising': 'Many findings seem obvious in retrospect, but this does not mean that the community is already aware of them and can use them as building blocks for future work.',
'The results contradict what I would expect': 'You may be a victim of confirmation bias, and be unwilling to accept data contradicting your prior beliefs.',
'The results are not novel': 'Such broad claims need to be backed up with references.',
'This has no precedent in existing literature': 'Believe it or not: papers that are more novel tend to be harder to publish. Reviewers may be unnecessarily conservative.',
'The results do not surpass the latest SOTA', 'SOTA results are neither necessary nor sufficient for a scientific contribution. An engineering paper could also offer improvements on other dimensions (efficiency, generalizability, interpretability, fairness, etc.',
'The results are negative': 'The bias towards publishing only positive results is a known problem in many fields, and contributes to hype and overclaiming. If something systematically does not work where it could be expected to, the community does need to know about it.',
'This method is too simple': 'The goal is to solve the problem, not to solve it in a complex way. Simpler solutions are in fact preferable, as they are less brittle and easier to deploy in real-world settings.',
'The paper doesn't use [my preferred methodology], e.g., deep learning': 'NLP is an interdisciplinary field, relying on many kinds of contributions: models, resource, survey, data/linguistic/social analysis, position, and theory.',
'The topic is too niche/ Narrow Topics': 'It is easier to publish on trendy,‘scientifically sexy’ topics (Smith, 2010). In the last two years, there has been little talk of anything other than large pretrained Transformers,
with BERT alone becoming the target of over 150 studies proposing analysis and various modifications (Rogers et al., 2020). The ‘hot trend’ forms the prototype for the kind of paper that should be
recommended for acceptance. Niche topics such as historical text normalization are downvoted (unless, of course, BERT could somehow be used for that).',
'The approach is tested only on [not English], so unclear if it will generalize to other languages': 'The same is true of NLP research that tests only on English. Monolingual work on any language is important both practically (methods and resources for that language) and theoretically (potentially contributing to deeper understanding of language in general)',
'The paper has language errors/ Writing style': 'As long as the writing is clear enough, better scientific content should be more valuable than better journalistic skills. If it comes in the comments, suggestions and typos, not lazy. The paper’s language or writing style. Please focus on the paper’s substance. We understand that there may be times when the language or writing style is so poor that reviewers can not understand the paper’s content and substance. In that case, it is fine to reject the paper, however you should only do so after making a concerted effort to understand the paper.',
'The paper is missing the comparison to the [latest X]': 'Per ACL policy, the authors are not obliged to draw comparisons with contemporaneous work, i.e., work published within three months before the submission (or three months before a re-submission).',
'The authors could also do [extra experiment X]': 'It is always possible to come up with extra experiments and follow-up work. This is fair if the experiments that are already presented are insufficient for the claim that the authors are making. But any other extra experiments are in the “nice-to-have” category, and belong in the “suggestions” section rather than “weaknesses.”',
'The authors should have done [X] instead': 'A.k.a. “I would have written a different paper.” There are often several valid approaches to a problem. This criticism applies only if the authors’ choices prevent them from answering their research question, their framing is misleading, or the question is not worth asking. If not, then [X] is a comment or a suggestion, but not a “weakness.”',
'Not Enough Info': 'Problematic but not sure how to verify from the given review'
'Non Mainstream approaches' : 'Since a ‘mainstream’ *ACL paper currently uses DL-based methods, anything else might look like it does not really
belong in the main track - even though ACL stands for ‘Association for Computational Linguistics’. That puts interdisciplinary efforts at a disadvantage,
and continues the trend for intellectual segregation of NLP (Reiter, 2007). E.g., theoretical papers and linguistic resources should not be a priori at a
disadvantage just because they do not contain DL experiments.',
'Resource paper': 'The paper is a resource paper. In a field that relies on supervised machine learning as much as NLP, development of datasets is as important as modeling work. This blog post discusses what can and cannot be grounds for dismissing a resource paper' : ''
} 



Given a Full Review and a Target Sentence corresponding to that review, your task is to classify whether the target sentence is a lazy thinking sentence or not. 
If the target sentence falls into any of the above classes eg.,  `The topic is too niche' or `The results are not novel', the correct label would be "lazy thinking" 
or else the label should be "not problematic". You should only answer with the labels "lazy thinking" or "not problematic", not any other words.

Full Review : {{review}}


Target Sentence : {{weakness}}

'''

round2_prompt2_problematic = ''' As the number of scientific publications grows over the years, the need for efficient quality control in peer-reviewing 
becomes crucial. Due to the high reviewing load, the reviewers are often prone to different kinds of bias, which inherently contribute to 
lower reviewing quality and this overall hampers the scientific progress in the field. The ACL peer reviewing guidelines characterize some 
of such reviewing bias.  These are termed lazy thinking. The lazy thinking classes and the reason for them being problematic are provided below one after another:

'The results are not surprising':
'Many findings seem obvious in retrospect, but this does not mean that the community is already aware of them and can use them as building blocks for future work.',

'The results contradict what I would expect':
'You may be a victim of confirmation bias, and be unwilling to accept data contradicting your prior beliefs.',

'The results are not novel':
'Such broad claims need to be backed up with references.',

'This has no precedent in existing literature':
'Believe it or not: papers that are more novel tend to be harder to publish. Reviewers may be unnecessarily conservative.',

'The results do not surpass the latest SOTA':
'SOTA results are neither necessary nor sufficient for a scientific contribution. An engineering paper could also offer improvements on other dimensions (efficiency, generalizability, interpretability, fairness, etc.',

'The results are negative':
'The bias towards publishing only positive results is a known problem in many fields, and contributes to hype and overclaiming. If something systematically does not work where it could be expected to, the community does need to know about it.',

'This method is too simple':
'The goal is to solve the problem, not to solve it in a complex way. Simpler solutions are in fact preferable, as they are less brittle and easier to deploy in real-world settings.',

'The paper doesn't use [my preferred methodology], e.g., deep learning':
'NLP is an interdisciplinary field, relying on many kinds of contributions: models, resource, survey, data/linguistic/social analysis, position, and theory.',

'The topic is too niche/ Narrow Topics':
'It is easier to publish on trendy,‘scientifically sexy’ topics (Smith, 2010). In the last two years, there has been little talk of anything other than large pretrained Transformers,
with BERT alone becoming the target of over 150 studies proposing analysis and various modifications (Rogers et al., 2020). The ‘hot trend’ forms the prototype for the kind of paper that should be
recommended for acceptance. Niche topics such as historical text normalization are downvoted (unless, of course, BERT could somehow be used for that).',

'The approach is tested only on [not English], so unclear if it will generalize to other languages':
'The same is true of NLP research that tests only on English. Monolingual work on any language is important both practically (methods and resources for that language) and theoretically (potentially contributing to deeper understanding of language in general)',

'The paper has language errors/ Writing style':
'As long as the writing is clear enough, better scientific content should be more valuable than better journalistic skills. If it comes in the comments, suggestions and typos, not lazy. The paper’s language or writing style. Please focus on the paper’s substance. We understand that there may be times when the language or writing style is so poor that reviewers can not understand the paper’s content and substance. In that case, it is fine to reject the paper, however you should only do so after making a concerted effort to understand the paper.',

'The paper is missing the comparison to the [latest X]': 
'Per ACL policy, the authors are not obliged to draw comparisons with contemporaneous work, i.e., work published within three months before the submission (or three months before a re-submission).',

'The authors could also do [extra experiment X]': 
'It is always possible to come up with extra experiments and follow-up work. This is fair if the experiments that are already presented are insufficient for the claim that the authors are making. But any other extra experiments are in the “nice-to-have” category, and belong in the “suggestions” section rather than “weaknesses.”',

'The authors should have done [X] instead': 
'A.k.a. “I would have written a different paper.” There are often several valid approaches to a problem. This criticism applies only if the authors’ choices prevent them from answering their research question, their framing is misleading, or the question is not worth asking. If not, then [X] is a comment or a suggestion, but not a “weakness.”',

'None': 
'This is not lazy thinking',

'Not Enough Info': 
'Problematic but not sure how to verify from the given review'

'Non Mainstream approaches' : 
'Since a ‘mainstream’ *ACL paper currently uses DL-based methods, anything else might look like it does not really
belong in the main track - even though ACL stands for ‘Association for Computational Linguistics’. That puts interdisciplinary efforts at a disadvantage,
and continues the trend for intellectual segregation of NLP (Reiter, 2007). E.g., theoretical papers and linguistic resources should not be a priori at a
disadvantage just because they do not contain DL experiments.',

'Resource paper': 
'The paper is a resource paper. In a field that relies on supervised machine learning as much as NLP, development of datasets is as important as modeling work. This blog post discusses what can and cannot be grounds for dismissing a resource paper'



Given a Full Review and a Target Sentence corresponding to that review, your task is to classify whether the target sentence is a lazy thinking sentence or not. 
If the target sentence falls into any of the above classes eg.,  `The topic is too niche' or `The results are not novel', the correct label would be "lazy thinking" 
or else the label should be "not problematic". You should only answer with the labels "lazy thinking" or "not problematic", not any other words.

Full Review : {{review}}
Target Sentence : {{weakness}}

'''

round2_prompt3_problematic = '''Lazy thinking classes and their definitions:

"The results are not surprising": Findings may seem obvious later, but the community might not be aware of them.
"The results contradict my expectations": Acknowledging potential confirmation bias when results oppose prior beliefs.
"The results are not novel": Broad claims requiring supporting references.
"No precedent in existing literature": Novel papers face conservative reviewer bias.
"The results do not surpass the latest SOTA": SOTA results are not the sole criterion for contribution; improvements in efficiency, generalizability, etc. are also valid.
"The results are negative": Bias toward positive results; community needs to know about consistent failures too.
"The method is too simple": Simpler solutions are preferable for real-world deployment.
"The paper doesn't use my preferred methodology": NLP relies on diverse contributions beyond specific methods like deep learning.
"The topic is too niche/ Narrow Topics": Trendy topics are easier to publish; niche topics are undervalued.
"The approach is language-specific": Monolingual work is important for practical and theoretical reasons.
"The paper has language errors/ Writing style": Scientific content takes precedence over journalistic skills; reject only if language obscures content.
"The paper misses a comparison": Authors are not obliged to compare with contemporaneous work per ACL policy.
"The authors could do extra experiments": Differentiate between necessary and "nice-to-have" experiments.
"The authors should have done X instead": Recognize multiple valid approaches; criticism applies if choices hinder research questions.
"None": Not lazy thinking.
"Not Enough Info": Problematic, but verification challenging.
"Non Mainstream approaches" : 'Since a ‘mainstream’ *ACL paper currently uses DL-based methods, anything else might look like it does not really
belong in the main track - even though ACL stands for ‘Association for Computational Linguistics’. That puts interdisciplinary efforts at a disadvantage,
and continues the trend for intellectual segregation of NLP (Reiter, 2007). E.g., theoretical papers and linguistic resources should not be a priori at a
disadvantage just because they do not contain DL experiments.',
"Resource paper": 'The paper is a resource paper. In a field that relies on supervised machine learning as much as NLP, development of datasets is as important as modeling work. This blog post discusses what can and cannot be grounds for dismissing a resource paper'

Task: Classify target sentences from full reviews into lazy thinking or not problematic classes.


Full Review : {{review}}
Target Sentence : {{weakness}}

'''


round2_prompt_problematic_only_eg = ''' As the number of scientific publications grows over the years, the need for efficient quality control in peer-reviewing 
becomes crucial. Due to the high reviewing load, the reviewers are often prone to different kinds of bias, which inherently contribute to 
lower reviewing quality and this overall hampers the scientific progress in the field. The ACL peer reviewing guidelines characterize some 
of such reviewing bias.  These are termed lazy thinking. The lazy thinking classes, their meaning and the reason for them being problematic 
are provided as a dictionary in the format ```key: meaning: reason for being problematic```. If a meaning or reason for being problematic is not known,
'' is provided in that place: 


{'The results are not surprising': 'Many findings seem obvious in retrospect, but this does not mean that the community is already aware of them and can use them as building blocks for future work.',
'The results contradict what I would expect': 'You may be a victim of confirmation bias, and be unwilling to accept data contradicting your prior beliefs.',
'The results are not novel': 'Such broad claims need to be backed up with references.',
'This has no precedent in existing literature': 'Believe it or not: papers that are more novel tend to be harder to publish. Reviewers may be unnecessarily conservative.',
'The results do not surpass the latest SOTA', 'SOTA results are neither necessary nor sufficient for a scientific contribution. An engineering paper could also offer improvements on other dimensions (efficiency, generalizability, interpretability, fairness, etc.',
'The results are negative': 'The bias towards publishing only positive results is a known problem in many fields, and contributes to hype and overclaiming. If something systematically does not work where it could be expected to, the community does need to know about it.',
'This method is too simple': 'The goal is to solve the problem, not to solve it in a complex way. Simpler solutions are in fact preferable, as they are less brittle and easier to deploy in real-world settings.',
'The paper doesn't use [my preferred methodology], e.g., deep learning': 'NLP is an interdisciplinary field, relying on many kinds of contributions: models, resource, survey, data/linguistic/social analysis, position, and theory.',
'The topic is too niche/ Narrow Topics': 'It is easier to publish on trendy,‘scientifically sexy’ topics (Smith, 2010). In the last two years, there has been little talk of anything other than large pretrained Transformers,
with BERT alone becoming the target of over 150 studies proposing analysis and various modifications (Rogers et al., 2020). The ‘hot trend’ forms the prototype for the kind of paper that should be
recommended for acceptance. Niche topics such as historical text normalization are downvoted (unless, of course, BERT could somehow be used for that).',
'The approach is tested only on [not English], so unclear if it will generalize to other languages': 'The same is true of NLP research that tests only on English. Monolingual work on any language is important both practically (methods and resources for that language) and theoretically (potentially contributing to deeper understanding of language in general)',
'The paper has language errors/ Writing style': 'As long as the writing is clear enough, better scientific content should be more valuable than better journalistic skills. If it comes in the comments, suggestions and typos, not lazy. The paper’s language or writing style. Please focus on the paper’s substance. We understand that there may be times when the language or writing style is so poor that reviewers can not understand the paper’s content and substance. In that case, it is fine to reject the paper, however you should only do so after making a concerted effort to understand the paper.',
'The paper is missing the comparison to the [latest X]': 'Per ACL policy, the authors are not obliged to draw comparisons with contemporaneous work, i.e., work published within three months before the submission (or three months before a re-submission).',
'The authors could also do [extra experiment X]': 'It is always possible to come up with extra experiments and follow-up work. This is fair if the experiments that are already presented are insufficient for the claim that the authors are making. But any other extra experiments are in the “nice-to-have” category, and belong in the “suggestions” section rather than “weaknesses.”',
'The authors should have done [X] instead': 'A.k.a. “I would have written a different paper.” There are often several valid approaches to a problem. This criticism applies only if the authors’ choices prevent them from answering their research question, their framing is misleading, or the question is not worth asking. If not, then [X] is a comment or a suggestion, but not a “weakness.”',
'Not Enough Info': 'Problematic but not sure how to verify from the given review'
'Non Mainstream approaches' : 'Since a ‘mainstream’ *ACL paper currently uses DL-based methods, anything else might look like it does not really
belong in the main track - even though ACL stands for ‘Association for Computational Linguistics’. That puts interdisciplinary efforts at a disadvantage,
and continues the trend for intellectual segregation of NLP (Reiter, 2007). E.g., theoretical papers and linguistic resources should not be a priori at a
disadvantage just because they do not contain DL experiments.',
'Resource paper': 'The paper is a resource paper. In a field that relies on supervised machine learning as much as NLP, development of datasets is as important as modeling work. This blog post discusses what can and cannot be grounds for dismissing a resource paper' : ''
} 

Task: Classify target sentences from full reviews into lazy thinking or not problematic classes.

Target Sentence : {{weakness}}

'''

round2_prompt2_problematic_only_eg = ''' As the number of scientific publications grows over the years, the need for efficient quality control in peer-reviewing 
becomes crucial. Due to the high reviewing load, the reviewers are often prone to different kinds of bias, which inherently contribute to 
lower reviewing quality and this overall hampers the scientific progress in the field. The ACL peer reviewing guidelines characterize some 
of such reviewing bias.  These are termed lazy thinking. The lazy thinking classes and the reason for them being problematic are provided below one after another:

'The results are not surprising':
'Many findings seem obvious in retrospect, but this does not mean that the community is already aware of them and can use them as building blocks for future work.',

'The results contradict what I would expect':
'You may be a victim of confirmation bias, and be unwilling to accept data contradicting your prior beliefs.',

'The results are not novel':
'Such broad claims need to be backed up with references.',

'This has no precedent in existing literature':
'Believe it or not: papers that are more novel tend to be harder to publish. Reviewers may be unnecessarily conservative.',

'The results do not surpass the latest SOTA':
'SOTA results are neither necessary nor sufficient for a scientific contribution. An engineering paper could also offer improvements on other dimensions (efficiency, generalizability, interpretability, fairness, etc.',

'The results are negative':
'The bias towards publishing only positive results is a known problem in many fields, and contributes to hype and overclaiming. If something systematically does not work where it could be expected to, the community does need to know about it.',

'This method is too simple':
'The goal is to solve the problem, not to solve it in a complex way. Simpler solutions are in fact preferable, as they are less brittle and easier to deploy in real-world settings.',

'The paper doesn't use [my preferred methodology], e.g., deep learning':
'NLP is an interdisciplinary field, relying on many kinds of contributions: models, resource, survey, data/linguistic/social analysis, position, and theory.',

'The topic is too niche/ Narrow Topics':
'It is easier to publish on trendy,‘scientifically sexy’ topics (Smith, 2010). In the last two years, there has been little talk of anything other than large pretrained Transformers,
with BERT alone becoming the target of over 150 studies proposing analysis and various modifications (Rogers et al., 2020). The ‘hot trend’ forms the prototype for the kind of paper that should be
recommended for acceptance. Niche topics such as historical text normalization are downvoted (unless, of course, BERT could somehow be used for that).',

'The approach is tested only on [not English], so unclear if it will generalize to other languages':
'The same is true of NLP research that tests only on English. Monolingual work on any language is important both practically (methods and resources for that language) and theoretically (potentially contributing to deeper understanding of language in general)',

'The paper has language errors/ Writing style':
'As long as the writing is clear enough, better scientific content should be more valuable than better journalistic skills. If it comes in the comments, suggestions and typos, not lazy. The paper’s language or writing style. Please focus on the paper’s substance. We understand that there may be times when the language or writing style is so poor that reviewers can not understand the paper’s content and substance. In that case, it is fine to reject the paper, however you should only do so after making a concerted effort to understand the paper.',

'The paper is missing the comparison to the [latest X]': 
'Per ACL policy, the authors are not obliged to draw comparisons with contemporaneous work, i.e., work published within three months before the submission (or three months before a re-submission).',

'The authors could also do [extra experiment X]': 
'It is always possible to come up with extra experiments and follow-up work. This is fair if the experiments that are already presented are insufficient for the claim that the authors are making. But any other extra experiments are in the “nice-to-have” category, and belong in the “suggestions” section rather than “weaknesses.”',

'The authors should have done [X] instead': 
'A.k.a. “I would have written a different paper.” There are often several valid approaches to a problem. This criticism applies only if the authors’ choices prevent them from answering their research question, their framing is misleading, or the question is not worth asking. If not, then [X] is a comment or a suggestion, but not a “weakness.”',

'None': 
'This is not lazy thinking',

'Not Enough Info': 
'Problematic but not sure how to verify from the given review'

'Non Mainstream approaches' : 
'Since a ‘mainstream’ *ACL paper currently uses DL-based methods, anything else might look like it does not really
belong in the main track - even though ACL stands for ‘Association for Computational Linguistics’. That puts interdisciplinary efforts at a disadvantage,
and continues the trend for intellectual segregation of NLP (Reiter, 2007). E.g., theoretical papers and linguistic resources should not be a priori at a
disadvantage just because they do not contain DL experiments.',

'Resource paper': 
'The paper is a resource paper. In a field that relies on supervised machine learning as much as NLP, development of datasets is as important as modeling work. This blog post discusses what can and cannot be grounds for dismissing a resource paper'



Given a Target Sentence, your task is to classify whether the target sentence is a lazy thinking sentence or not. 
If the target sentence falls into any of the above classes eg.,  `The topic is too niche' or `The results are not novel', the correct label would be "lazy thinking" 
or else the label should be "not problematic". You should only answer with the labels "lazy thinking" or "not problematic", not any other words.

Target Sentence : {{weakness}}

'''

round2_prompt3_problematic_only_eg = '''Lazy thinking classes and their definitions:

"The results are not surprising": Findings may seem obvious later, but the community might not be aware of them.
"The results contradict my expectations": Acknowledging potential confirmation bias when results oppose prior beliefs.
"The results are not novel": Broad claims requiring supporting references.
"No precedent in existing literature": Novel papers face conservative reviewer bias.
"The results do not surpass the latest SOTA": SOTA results are not the sole criterion for contribution; improvements in efficiency, generalizability, etc. are also valid.
"The results are negative": Bias toward positive results; community needs to know about consistent failures too.
"The method is too simple": Simpler solutions are preferable for real-world deployment.
"The paper doesn't use my preferred methodology": NLP relies on diverse contributions beyond specific methods like deep learning.
"The topic is too niche/ Narrow Topics": Trendy topics are easier to publish; niche topics are undervalued.
"The approach is language-specific": Monolingual work is important for practical and theoretical reasons.
"The paper has language errors/ Writing style": Scientific content takes precedence over journalistic skills; reject only if language obscures content.
"The paper misses a comparison": Authors are not obliged to compare with contemporaneous work per ACL policy.
"The authors could do extra experiments": Differentiate between necessary and "nice-to-have" experiments.
"The authors should have done X instead": Recognize multiple valid approaches; criticism applies if choices hinder research questions.
"None": Not lazy thinking.
"Not Enough Info": Problematic, but verification challenging.
"Non Mainstream approaches" : 'Since a ‘mainstream’ *ACL paper currently uses DL-based methods, anything else might look like it does not really
belong in the main track - even though ACL stands for ‘Association for Computational Linguistics’. That puts interdisciplinary efforts at a disadvantage,
and continues the trend for intellectual segregation of NLP (Reiter, 2007). E.g., theoretical papers and linguistic resources should not be a priori at a
disadvantage just because they do not contain DL experiments.',
"Resource paper": 'The paper is a resource paper. In a field that relies on supervised machine learning as much as NLP, development of datasets is as important as modeling work. This blog post discusses what can and cannot be grounds for dismissing a resource paper'

Task: Classify target sentences into lazy thinking or not problematic classes.


Target Sentence : {{weakness}}

'''