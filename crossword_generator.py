import random
import requests
from bs4 import BeautifulSoup

class CrosswordGenerator:
    def __init__(self, words, clues, grid_size=15):
        self.words = sorted(words, key=len, reverse=True)
        self.clues = clues
        self.grid_size = grid_size
        self.grid = [['#' for _ in range(grid_size)] for _ in range(grid_size)]
        self.placed_words = []

    def _can_place_word(self, word, row, col, direction):
        word_len = len(word)

        if direction == 'H':
            if col + word_len > self.grid_size:
                return False

            for i in range(word_len):
                current_char = self.grid[row][col + i]
                if current_char != '#' and current_char != word[i]:
                    return False
                if row > 0 and self.grid[row - 1][col + i] != '#':
                    return False
                if row < self.grid_size - 1 and self.grid[row + 1][col + i] != '#':
                    return False
            if col > 0 and self.grid[row][col - 1] != '#':
                return False
            if col + word_len < self.grid_size and self.grid[row][col + word_len] != '#':
                return False

        elif direction == 'V':
            if row + word_len > self.grid_size:
                return False

            for i in range(word_len):
                current_char = self.grid[row + i][col]
                if current_char != '#' and current_char != word[i]:
                    return False
                if col > 0 and self.grid[row + i][col - 1] != '#':
                    return False
                if col < self.grid_size - 1 and self.grid[row + i][col + 1] != '#':
                    return False
            if row > 0 and self.grid[row - 1][col] != '#':
                return False
            if row + word_len < self.grid_size and self.grid[row + word_len] != '#':
                return False
        return True

    def _place_word(self, word, row, col, direction):
        if direction == 'H':
            for i in range(len(word)):
                self.grid[row][col + i] = word[i]
        elif direction == 'V':
            for i in range(len(word)):
                self.grid[row + i][col] = word[i]
        self.placed_words.append({"word": word, "row": row, "col": col, "direction": direction})
        return True

    def generate(self):
        for word in self.words:
            placed = False
            if not self.placed_words:
                # Place the first word in the center
                row = self.grid_size // 2
                col = self.grid_size // 2 - len(word) // 2
                self._place_word(word, row, col, 'H')
                placed = True
                continue

            for p_word_info in self.placed_words:
                p_word = p_word_info["word"]
                p_row = p_word_info["row"]
                p_col = p_word_info["col"]
                p_direction = p_word_info["direction"]

                for i, char1 in enumerate(word):
                    for j, char2 in enumerate(p_word):
                        if char1 == char2:
                            if p_direction == 'H':
                                new_row = p_row - i
                                new_col = p_col + j
                                if self._can_place_word(word, new_row, new_col, 'V'):
                                    self._place_word(word, new_row, new_col, 'V')
                                    placed = True
                                    break
                            else:
                                new_row = p_row + j
                                new_col = p_col - i
                                if self._can_place_word(word, new_row, new_col, 'H'):
                                    self._place_word(word, new_row, new_col, 'H')
                                    placed = True
                                    break
                    if placed:
                        break
            
            if not placed:
                # Could not place the word
                print(f"Could not place word: {word}")

    def get_crossword(self):
        horizontal_clues = []
        vertical_clues = []
        number = 1
        for word_info in self.placed_words:
            clue_text = self.clues.get(word_info["word"])
            if word_info["direction"] == 'H':
                horizontal_clues.append({"number": number, "clue": clue_text})
            else:
                vertical_clues.append({"number": number, "clue": clue_text})
            word_info["number"] = number
            number += 1
        return {"grid": self.grid, "clues": {"horizontal": horizontal_clues, "vertical": vertical_clues}, "placed_words": self.placed_words}


URLS = {
    "constitucional": "https://www.planalto.gov.br/ccivil_03/constituicao/constituicao.htm",
    "penal": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del2848compilado.htm",
    "civil": "https://www.planalto.gov.br/ccivil_03/leis/2002/l10406compilada.htm",
    "processual_civil": "https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2015/lei/l13105.htm",
    "tributario": "https://www.planalto.gov.br/ccivil_03/leis/l5172compilado.htm",
    "previdenciario": "https://www.planalto.gov.br/ccivil_03/leis/l8213cons.htm",
    "administrativo": "https://www.planalto.gov.br/ccivil_03/leis/l9784.htm",
    "processual_penal": "https://www.planalto.gov.br/ccivil_03/decreto-lei/del3689.htm"
}

def generate_crossword_data(subject):
    if subject == "misto":
        words_and_clues = {}
        for s in URLS.keys():
            words_and_clues.update(fetch_and_extract_words(s))
    else:
        words_and_clues = fetch_and_extract_words(subject)

    if not words_and_clues:
        return {"grid": [], "clues": {"horizontal": [], "vertical": []}}

    words = list(words_and_clues.keys())
    clues = words_and_clues

    generator = CrosswordGenerator(words, clues)
    generator.generate()
    return generator.get_crossword()


def fetch_and_extract_words(subject):
    # For now, we'll return some sample words.
    sample_words = {
        "constitucional": {"constituicao": "Lei fundamental do país.", "senado": "Câmara alta do Congresso Nacional."},
        "penal": {"crime": "Infração de maior potencial ofensivo.", "pena": "Sanção imposta pelo Estado."},
        "civil": {"casamento": "União legal entre duas pessoas.", "contrato": "Acordo de vontades."},
        "processual_civil": {"peticao": "Peça processual inicial.", "sentenca": "Decisão do juiz."},
        "tributario": {"imposto": "Tributo obrigatório.", "taxa": "Tributo por serviço específico."},
        "previdenciario": {"aposentadoria": "Afastamento remunerado do trabalho.", "contribuicao": "Pagamento para a previdência."},
        "administrativo": {"licitacao": "Processo de compra do governo.", "servidor": "Funcionário público."},
        "processual_penal": {"habeascorpus": "Garantia contra prisão ilegal.", "inquerito": "Investigação policial."}
    }

    return sample_words.get(subject, {})
