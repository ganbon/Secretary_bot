import torch
from transformers import BertForSequenceClassification,BertJapaneseTokenizer
def generate(input, max_length = 50):
    emotion = ['😊', '😲', '😟', '😡', '😧', '🙂']
    model_path = 'model_emotion'
    tokenizer = BertJapaneseTokenizer.from_pretrained(model_path)
    train_model = BertForSequenceClassification.from_pretrained(model_path, num_labels = 5)
    data = tokenizer(input,max_length = max_length,truncation = True, padding = 'longest', return_tensors = 'pt')
    output = train_model.forward(
        input_ids = data['input_ids'],
        attention_mask = data['attention_mask'],
        labels = None
    )
    result = output.logits
    score = torch.argmax(result)
    if result[0][score] > 2:
        return emotion[int(score)]
    else:
        return emotion[5]
    
