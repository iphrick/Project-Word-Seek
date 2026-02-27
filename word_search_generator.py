import random

def create_grid(rows, cols):
    """
    Creates an empty grid filled with placeholder characters.
    """
    return [['-' for _ in range(cols)] for _ in range(rows)]

def can_place_word(grid, word, row, col, dr, dc):
    """
    Checks if a word can be placed at a given position and direction.
    dr, dc represent the direction (delta row, delta column).
    """
    rows = len(grid)
    cols = len(grid[0])
    word_len = len(word)

    for i in range(word_len):
        r, c = row + i * dr, col + i * dc
        if not (0 <= r < rows and 0 <= c < cols):
            return False  # Out of bounds
        if grid[r][c] != '-' and grid[r][c] != word[i]:
            return False  # Conflict with existing letter
    return True

def place_word(grid, word, row, col, dr, dc):
    """
    Places a word in the grid at the specified position and direction.
    """
    for i in range(len(word)):
        r, c = row + i * dr, col + i * dc
        grid[r][c] = word[i]

def fill_empty_cells(grid):
    """
    Fills any remaining empty cells with random uppercase letters.
    """
    for r_idx, row in enumerate(grid):
        for c_idx, cell in enumerate(row):
            if cell == '-':
                grid[r_idx][c_idx] = random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

def generate_word_search_data(words, rows, cols, max_attempts_per_word=50):
    """
    Generates a word search puzzle.
    """
    grid = create_grid(rows, cols)
    
    # Define possible directions: (dr, dc)
    # Horizontal, Vertical, Diagonal (top-left to bottom-right), Diagonal (top-right to bottom-left)
    # Also include reverse directions
    directions = [
        (0, 1), (0, -1),  # Horizontal (right, left)
        (1, 0), (-1, 0),  # Vertical (down, up)
        (1, 1), (-1, -1), # Diagonal (down-right, up-left)
        (1, -1), (-1, 1)  # Diagonal (down-left, up-right)
    ]

    placed_words = {}

    for word in words:
        word = word.upper()
        placed = False
        attempts = 0
        while not placed and attempts < max_attempts_per_word:
            dr, dc = random.choice(directions)
            start_row = random.randint(0, rows - 1)
            start_col = random.randint(0, cols - 1)

            if can_place_word(grid, word, start_row, start_col, dr, dc):
                place_word(grid, word, start_row, start_col, dr, dc)
                placed = True
                placed_words[word] = {
                    "row": start_row,
                    "col": start_col,
                    "dr": dr,
                    "dc": dc
                }
            attempts += 1
        if not placed:
            print(f"Warning: Could not place word '{word}' after {max_attempts_per_word} attempts.")

    fill_empty_cells(grid)
    return {"grid": grid, "words": list(words), "placed_words": placed_words}

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

def fetch_and_extract_words(subject):
    # For now, we'll return some sample words.
    sample_words = {
        "constitucional": ["constituicao", "senado"],
        "penal": ["crime", "pena"],
        "civil": ["casamento", "contrato"],
        "processual_civil": ["peticao", "sentenca"],
        "tributario": ["imposto", "taxa"],
        "previdenciario": ["aposentadoria", "contribuicao"],
        "administrativo": ["licitacao", "servidor"],
        "processual_penal": ["habeascorpus", "inquerito"]
    }

    return sample_words.get(subject, [])

def generate_word_search(subject, num_words=10):
    if subject == "misto":
        words = []
        for s in URLS.keys():
            words.extend(fetch_and_extract_words(s))
    else:
        words = fetch_and_extract_words(subject)

    if not words:
        return {"grid": [], "words": []}

    random.shuffle(words)
    words = words[:num_words]

    return generate_word_search_data(words, 15, 15)
