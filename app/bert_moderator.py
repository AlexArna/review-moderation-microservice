import pandas as pd
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import torch
from torch.utils.data import Dataset

# 1. Load and preprocess data
train_df = pd.read_csv('merged_train.csv')
val_df = pd.read_csv('merged_val.csv')
test_df = pd.read_csv('merged_test.csv')

labels = ["clean", "profanity", "spam"]
le = LabelEncoder()
le.fit(labels)
train_df['label_enc'] = le.transform(train_df['label'])
val_df['label_enc'] = le.transform(val_df['label'])
test_df['label_enc'] = le.transform(test_df['label'])

# 2. Prepare Dataset
class TextDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=128):
        self.encodings = tokenizer(texts, truncation=True, padding=True, max_length=max_len)
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

train_dataset = TextDataset(train_df['text'].tolist(), train_df['label_enc'].tolist(), tokenizer)
val_dataset = TextDataset(val_df['text'].tolist(), val_df['label_enc'].tolist(), tokenizer)
test_dataset = TextDataset(test_df['text'].tolist(), test_df['label_enc'].tolist(), tokenizer)

# 3. Load Pre-trained BERT
bert_model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=len(labels))

# 4. Training setup
training_args = TrainingArguments(
    output_dir='./results',
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=32,
    evaluation_strategy="epoch",
    save_strategy="epoch",
    logging_dir='./logs',
    logging_steps=100,
    load_best_model_at_end=True,
    metric_for_best_model="eval_loss"
)

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    preds = logits.argmax(-1)
    return {
        'classification_report': classification_report(labels, preds, target_names=labels, output_dict=True)
    }

trainer = Trainer(
    model=bert_model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=val_dataset,
    compute_metrics=None  # We'll do classification_report separately for better formatting
)

# 5. Train
trainer.train()

# 6. Evaluate
y_pred = trainer.predict(test_dataset).predictions.argmax(-1)
y_true = test_df['label_enc'].values

print(classification_report(y_true, y_pred, target_names=labels))
print("Confusion matrix:")
print(confusion_matrix(y_true, y_pred))

# 7. Save model and tokenizer
save_dir = "./bert_moderation_model"
bert_model.save_pretrained(save_dir)
tokenizer.save_pretrained(save_dir)
print(f"Model and tokenizer saved to {save_dir}")