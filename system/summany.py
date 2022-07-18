from transformers import T5Tokenizer,T5ForConditionalGeneration


def generate_text_from_model(text_file, max_length_src = 700, max_length_target = 70, num_return_sequences = 3):
    model_path = 'model/model_summany'
    tokenizer = T5Tokenizer.from_pretrained(model_path)
    with open(text_file,'r',encoding='UTF-8') as f:
        text = f.read()
    train_model = T5ForConditionalGeneration.from_pretrained(model_path)
    train_model.eval()
    batch = tokenizer([text], max_length = max_length_src, truncation = True, padding = 'longest', return_tensors = 'pt')

    # 生成処理を行う
    outputs = train_model.generate(input_ids = batch['input_ids'], attention_mask = batch['attention_mask'], max_length = max_length_target,
                                    repetition_penalty = 8.0, num_return_sequences = num_return_sequences)

    generated_texts = [tokenizer.decode(ids, skip_special_tokens = True, clean_up_tokenization_spaces = False) for ids in outputs]
    return generated_texts