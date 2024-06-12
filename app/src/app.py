import sys
import random
import torch
from PyQt5.QtWidgets import QLabel, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtCore import Qt  # Import Qt module for alignment constants
from utils import load_quotes, generate_sentence, build_vocab, max_words
from model import LanguageModel

class QuoteApp(QWidget):
    def __init__(self):
        super().__init__()
        
        print("Loading quotes")
        self.quotes = load_quotes('desala.txt')
        print("Building vocab")
        self.word_to_index, self.index_to_word = build_vocab(self.quotes)
        
        # Load the checkpoint
        print("Loading checkpoint")
        model_path = "desala.pth"
        checkpoint = torch.load(model_path, map_location=torch.device('cpu'))

        # Initialize your model and load state_dict
        print("Initializing model")
        vocab_size = len(self.word_to_index) + 1
        embed_size = 128
        hidden_size = 256
        num_layers = 2

        self.model = LanguageModel(vocab_size, embed_size, hidden_size, num_layers)  # Assuming LanguageModel is your model class
        self.model.load_state_dict(checkpoint)

        # Set model to evaluation mode
        self.model.eval()

        print("Initiating UI")
        self.initUI()

    def initUI(self):

        self.setWindowTitle('Desala Generator')

        layout = QVBoxLayout()

        self.title_label = QLabel('Your Daily Dose of Pollack', self)
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        self.prompt_input = QLineEdit(self)
        self.prompt_input.setPlaceholderText('Enter your prompt...')
        layout.addWidget(self.prompt_input)

        # Buttons layout
        buttons_layout = QHBoxLayout()

        # Search button
        self.search_button = QPushButton('Search', self)
        self.search_button.clicked.connect(self.on_search_click)
        buttons_layout.addWidget(self.search_button)

        # Generate button
        self.generate_button = QPushButton('Generate', self)
        self.generate_button.clicked.connect(self.on_generate_click)
        buttons_layout.addWidget(self.generate_button)

        # Set buttons to be equal in length
        self.search_button.setSizePolicy(self.generate_button.sizePolicy())

        layout.addLayout(buttons_layout)

        self.output_field = QTextEdit(self)
        self.output_field.setReadOnly(True)
        layout.addWidget(self.output_field)

        self.setLayout(layout)

    def on_generate_click(self):
        prompt = self.prompt_input.text()
        generated_sentence = generate_sentence(self.model, self.word_to_index, self.index_to_word, prompt, random.randint(1, 50))
        self.output_field.setPlainText(generated_sentence)

    def on_search_click(self):
        prompt = self.prompt_input.text().strip()
        random.shuffle(self.quotes)
        if prompt:
            for quote in self.quotes:
                if prompt.lower() in quote.lower():
                    self.output_field.setPlainText(quote)
                    return
        else:
            self.output_field.setPlainText(self.quotes[0])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QuoteApp()
    window.show()
    sys.exit(app.exec_())
