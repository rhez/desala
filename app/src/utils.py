from torch.utils.data import Dataset
import torch
import random

def load_quotes(file_path):
    with open(file_path, 'r') as file:
        quotes = file.readlines()
    return [quote.strip() for quote in quotes if quote.strip()]

def max_words(quotes):
    return max(len(quote.split()) for quote in quotes)

def build_vocab(quotes):
    """
    Build the vocabulary from a list of quotes.
    Returns:
    - word_to_index: a dictionary mapping each word to a unique index
    - index_to_word: a dictionary mapping each index to the corresponding word
    """
    vocab = ['<pad>', '<bos>', '<eos>', '<unk>']
    word_to_index = {word: idx for idx, word in enumerate(vocab)}
    index_to_word = {idx: word for idx, word in enumerate(vocab)}

    for quote in quotes:
        for word in quote.split():
            if word not in word_to_index:
                idx = len(word_to_index)
                word_to_index[word] = idx
                index_to_word[idx] = word

    return word_to_index, index_to_word

class QuotesDataset(Dataset):
    def __init__(self, word_to_index, index_to_word, file_path):
        self.word_to_index = word_to_index
        self.index_to_word = index_to_word
        self.quotes = load_quotes(file_path)

    def __len__(self):
        return len(self.quotes)

    def __getitem__(self, idx):
        words = self.quotes[idx].split()
        indices = [self.word_to_index.get(word, self.word_to_index['<unk>']) for word in words]
        return torch.tensor(indices, dtype=torch.long)

def generate_sentence(model, word_to_index, index_to_word, prompt='', max_length=20):
    model.eval()
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    with torch.no_grad():
        if not prompt.strip():  # Check if prompt is empty or consists of whitespace
            # Generate a random prompt word from vocabulary
            r_i = random.randint(0, len(index_to_word) - 1)
            prompt = index_to_word[r_i]
        
        encoded_token = [word_to_index.get(word, word_to_index['<unk>']) for word in prompt.split()]
        if encoded_token[0] == word_to_index['<unk>']:
            # Choose a random word from the vocabulary
            r_i = random.randint(0, len(index_to_word) - 1)
            prompt = index_to_word[r_i]
            encoded_token = [word_to_index[prompt]]

        encoded_token = torch.tensor(encoded_token, dtype=torch.long).unsqueeze(0).to(device)
        hidden = model.init_hidden(1)
        
        for _ in range(max_length - len(encoded_token[0])):
            output, hidden = model(encoded_token, hidden)
            next_token_probs = torch.softmax(output[:, -1, :], dim=-1).squeeze()
            next_token_idx = torch.multinomial(next_token_probs, 1).item()
            next_token = torch.tensor([[next_token_idx]], dtype=torch.long).to(device)
            encoded_token = torch.cat((encoded_token, next_token), dim=1)
            if next_token_idx == word_to_index['<pad>']:
                break
        
        generated_words = [index_to_word[idx.item()] for idx in encoded_token[0]]
        return ' '.join(generated_words)
