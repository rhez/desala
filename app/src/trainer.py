import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from utils import QuotesDataset, build_vocab, load_quotes
from model import LanguageModel

class Trainer:
    def __init__(self, model, dataset, batch_size, learning_rate, num_epochs, device):
        self.model = model
        self.dataset = dataset
        self.dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True, collate_fn=self.collate_fn)
        self.criterion = nn.CrossEntropyLoss(ignore_index=dataset.word_to_index['<pad>'])
        self.optimizer = optim.Adam(model.parameters(), lr=learning_rate)
        self.num_epochs = num_epochs
        self.device = device

    def collate_fn(self, batch):
        max_length = max(len(seq) for seq in batch)
        padded_batch = [torch.cat([seq, torch.tensor([self.dataset.word_to_index['<pad>']] * (max_length - len(seq)), dtype=torch.long)]) for seq in batch]
        return torch.stack(padded_batch)

    def train(self):
        print("Begin training")
        self.model.to(self.device)
        for epoch in range(self.num_epochs):
            self.model.train()
            epoch_loss = 0
            for sequences in self.dataloader:
                sequences = sequences.to(self.device)
                hidden = self.model.init_hidden(sequences.size(0))
                self.optimizer.zero_grad()
                output, _ = self.model(sequences[:, :-1], hidden)
                loss = self.criterion(output.reshape(-1, output.size(2)), sequences[:, 1:].reshape(-1))
                loss.backward()
                self.optimizer.step()
                epoch_loss += loss.item()
            print(f"Epoch {epoch + 1}/{self.num_epochs}, Loss: {epoch_loss / len(self.dataloader)}")

if __name__ == "__main__":
    file_path = "desala.txt"
    quotes_list = load_quotes(file_path)
    word_to_index, index_to_word = build_vocab(quotes_list)
    vocab_size = len(word_to_index) + 1
    embedding_dim = 128
    hidden_dim = 256
    num_layers = 2
    batch_size = 32
    learning_rate = 0.001
    num_epochs = 20
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    dataset = QuotesDataset(word_to_index, index_to_word, file_path)
    model = LanguageModel(vocab_size, embedding_dim, hidden_dim, num_layers)
    trainer = Trainer(model, dataset, batch_size, learning_rate, num_epochs, device)
    trainer.train()

    # Save the model
    torch.save(model.state_dict(), "data/desala.pth")
    print("Model saved as desala.pth")
