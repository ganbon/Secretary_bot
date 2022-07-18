import torch
import torch.nn as nn
from transformers import BertForSequenceClassification,BertJapaneseTokenizer


#感情表現の評価
def generate(message, main_emotion, max_length = 50):
    emotion = ['😊', '😧','😡','😲','😞', '🙂']
    model_path = 'model/model_emotion_v3'
    sigmoid = nn.Sigmoid()
    tokenizer = BertJapaneseTokenizer.from_pretrained(model_path)
    train_model = BertForSequenceClassification.from_pretrained(model_path, num_labels = 5)
    data = tokenizer(message ,max_length = max_length,truncation = True, padding = 'longest', return_tensors = 'pt')
    output = train_model.forward(input_ids = data['input_ids'], attention_mask = data['attention_mask'], labels = None)
    now_emotion = output.logits[0]
    main_emotion = torch.tensor(main_emotion)
    save = torch.argmax(main_emotion)
    now = torch.argmax(now_emotion)
    if (main_emotion == torch.tensor([0,0,0,0,0])).all():
        main_emotion = now_emotion
    else:
        sub_emotion = (sigmoid(now_emotion)-0.5)*2
        for i in range(5):
            if save != now and now == i:
                main_emotion[i] += sub_emotion[i]+1
            elif save != now and save == i:
                main_emotion[i] += sub_emotion[i]-1
            else:
                main_emotion[i] += sub_emotion[i]
            if main_emotion[i].item() >= 5:
                main_emotion[i] = 5
            elif main_emotion[i].item() <= -5:
                main_emotion[i] = -5
    main_score = torch.argmax(main_emotion)
    if abs(main_emotion.max()) < 2:
        main_score = 5
    main_emotion = main_emotion.tolist()
    return emotion[int(main_score)], main_emotion


if __name__=='__main__':
    main_emotion = torch.zeros(5)
    while(1):
        a = input()
        result, main_emotion = generate(a, main_emotion)
        print(main_emotion)
        print(result)
    