from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments
from datasets import load_dataset

# 加載數據集
dataset = load_dataset('json', data_files={'train': 'train.json', 'test': 'test.json'})

# 加載分詞器和模型
model_name = "audreyt/Breeze-7B-Instruct-64k-v0.1-GGUF/Breeze-7B-Instruct-64k-v0.1-Q3_K_S.gguf"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# 進行數據預處理（如果需要）
def preprocess_function(examples):
    return tokenizer(examples['text'], truncation=True)

encoded_dataset = dataset.map(preprocess_function, batched=True)

# 設定訓練參數
training_args = TrainingArguments(
    output_dir='./results',
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
)

# 初始化Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=encoded_dataset['train'],
    eval_dataset=encoded_dataset['test'],
)

# 開始訓練
trainer.train()

# 保存模型
trainer.save_model('./my_model')
