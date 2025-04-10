## Dataset Details ##
The ```.json``` files that are downloaded will essential have the same format as shown below:

```JSON
 {
  "dataset": "lazy_reviewing_fine_grained_data",
  "id": "lazy_thinking_29",
  "messages": [
    {
    "role": "user",
    "content": "As the number of scientific publications grows over the years, the need for efficient quality control in peer-reviewing \nbecomes crucial. Due to the high reviewing load, the reviewers are often prone to different kinds of bias, which inherently contribute to \nlower reviewing quality and this overall hampers the scientific progress in the field. The ACL peer reviewing guidelines characterize some \nof such reviewing bias.  These are termed lazy thinking. The lazy thinking classes, their meaning and the reason for them being problematic \nare provided as a dictionary in the format ```key: meaning: reason for being problematic```. If a meaning or reason for being problematic is not known,\n'' is provided in that place: \n\n\n{'The results are not surprising': 'Many findings seem obvious in retrospect, but this does not mean that the community is already aware of them and can use them as building blocks for future work.',\n'The results contradict what I would expect': 'You may be a victim of confirmation bias, and be unwilling to accept data contradicting your prior beliefs.',\n'The results are not novel': 'Such broad claims need to be backed up with references.',\n'This has no precedent in existing literature': 'Believe it or not: papers that are more novel tend to be harder to publish. Reviewers may be unnecessarily conservative.'\n\n\n\nG\n\n\n\nGiven a target sentence, you need to classify the target sentence into one of the lazy thinking classes \neg., 'The topic is too niche', 'The results are negative'.\n\n\nTarget Sentence: Only Rouge-L is used for evaluation, which makes the evaluation not that reliable. Especially for some classification tasks, Rouge-L is not sensitive enough.\n\n"}
    }
    {"role":"assistant",
    "content":"The authors should have done [X] instead"
    }]
}
```
The fields in the ```.json``` files mean the following:

```dataset```: specifies the dataset task and type. In the above example it is the fine-grained lazy thinking detection task. The names can also be from the [SciRiff](https://huggingface.co/datasets/allenai/SciRIFF-train-mix) and [Tulu V2](https://huggingface.co/datasets/allenai/tulu-v2-sft-mixture) dataset. SciRiff and Tulu are collections with Supervised finetuning data from multiple datasets.

```messages```: We encode all the prompt and labels in the Jinja template format. The prompt, review and the task is passed within the ```"content"``` field for the ```"role":"user"```. The label is passed as the assistant's response within the ```"content"``` field for the ```"role":"assistant"```. 

```id```: This is the id for this instance.
