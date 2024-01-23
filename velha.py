import os
class Game:
    """
    This is the main class that is responsible for the game itself
    ...
    
    Attributes
    -----------------------------------------------------------------
    tabuleiro: tabuleiro
        responsible for the informations of the board
    
    jogador: list
        this attribute is the player of the game. The limit of players are 2
        
    turno: int
        this attribute indicates the turn of the game

    Methods
    -----------------------------------------------------------------
    player_round(jogador_atual): 
        Indicates the turn of the player based on it's symbol
        
    jogar:
        This method verifies if the game still going on and if there is a winner
    
    get_valid_move(jogador_atual):
        verifies if the movement is valid.
    
    validate_move(move):
        validates the movement of the player
    
    check_vitoria(jogador_symbol):
        verifies if any player has won
    
    record_result(vencedor):
        Generates the scoreboard in .txt
    
    game_over(jogador_symbol):
        Shows the message that the match has ended and saves which player has won 
    """
    def __init__(self, tabuleiro, p1, p2) -> None:
        """
        Parameter
        ----------------------------------------------
        tabuleiro: tabuleiro
            The object that represents the board
        
        p1: str
            Represents the first player
        
        p2: str
            Represents the second player
        """
        self.tabuleiro = tabuleiro
        self.jogador = [p1, p2]
        self.turno = 0
        self.score = {p1.symbol: 0, p2.symbol: 0}

    def player_round(self, jogador_atual):
        """
        
        This method annouces which player's round the match
        
        Parameter
        -------------
        jogador_atual: jogador_atual
            This object is the player that will be play in that round
        """
        print(f"Sua vez: {jogador_atual.symbol}")

    def jogar(self):
        """
        This method is the responsible for verify if the game will continue.
        if the game has a winner, it will call the method game over to say
        the game has ended.
        """
        sinalizador = False

        while not sinalizador:
            jogador_atual = self.jogador[self.turno]
            self.tabuleiro.print_tabuleiro()
            self.player_round(jogador_atual)

            movimento_do_jogador = self.get_valid_move(jogador_atual)

            self.tabuleiro.tiles[movimento_do_jogador] = jogador_atual.symbol

            vencedor = self.check_vitoria(jogador_atual.symbol)

            if vencedor:
                self.game_over(vencedor)
                sinalizador = True
            elif " " not in self.tabuleiro.tiles:
                print("Empate! O tabuleiro está cheio.")
                sinalizador = True
            else:
                self.turno = 1 - self.turno

    def get_valid_move(self, jogador_atual):
        """
        This method  validates if the movement is possible.
        """
        while True:
            try:
                move = int(input('Digite o local onde quer fazer a jogada: ')) - 1
                self.validate_move(move)
                return move
            except ValueError:
                print('Entrada inválida. Digite um número.')
            except InvalidMoveError as ime:
                print(f'Movimento inválido: {ime}')

    def validate_move(self, move):
        """
        This method is similar to the get_valid_moves, but this method confirms the movement of the player
        ...
        
        Parameter
        --------------
        
        move: int
            This attribute is the position on the matrix
        """
        if not (0 <= move < len(self.tabuleiro.tiles) and self.tabuleiro.tiles[move] == " "):
            raise InvalidMoveError('Movimento inválido. Tente novamente.')

    def check_vitoria(self, jogador_symbol):
        
        """
        This method checks if the game has ended
        
        Parameters
        ---------------------
        
        jogador_symbol: str
            This parameter is the player simbol
        
        """
        
        size = self.tabuleiro.size
        tiles = self.tabuleiro.tiles

        for i in range(size):
            # Vertical victory
            if all(tiles[i + j * size] == jogador_symbol for j in range(size)):
                return jogador_symbol

            # Horizontal victory
            if all(tiles[i * size + j] == jogador_symbol for j in range(size)):
                return jogador_symbol

        # Diagonal victories
        # Main diagonal
        if all(tiles[i * size + i] == jogador_symbol for i in range(size)):
            return jogador_symbol
        # Secondary diagonal
        if all(tiles[i * size + (size - 1 - i)] == jogador_symbol for i in range(size)):
            return jogador_symbol

        return False

    def record_result(self, vencedor):
        uppercased_symbol = vencedor.symbol.upper()
        self.score[uppercased_symbol] += 1
        file_path = os.path.join(os.getcwd(), 'scoreboard.txt')
        
        # Read existing content from the file
        existing_content = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                existing_content = file.readlines()

        # Update or add the player's score in the content
        player_info = f'Player: {uppercased_symbol}, Score: {self.score[uppercased_symbol]}\n'
        updated_content = [line for line in existing_content if not line.startswith(f'Player: {uppercased_symbol}, ')]
        updated_content.append(player_info)

        # Write the updated content back to the file
        with open(file_path, 'w') as file:
            file.writelines(updated_content)

        print("Current working directory:", os.getcwd())


    def game_over(self, jogador_symbol):
        """
        This method is responsible to announce that the mach has ended
        
        Parameter
        ---------------
        
        jogador_symbol: str
            Represent the symbol of the player
        
        """
        print(f'Acabou! Jogador com símbolo {jogador_symbol} ganhou!')
        self.record_result(self.jogador[self.turno])
 


class InvalidMoveError(Exception):
    """
    Class to identify if there's any movement error
    """
    pass


class Tabuleiro:
    """
    This class is responsible for create the board and while the match is happening and updates in every turn 
    ...
    
    Attributes
    ---------------------------------------------------------
    size: int
        it indicates the size of the board in the proporsion size x size
    
    Methods
    ---------------------------------------------------------
    print_tabuleiro:
        This method builds the board of the game proporcionally by the size that has been indicated
    
    """
    def __init__(self, size) -> None:
        """
        Constructor of the method Tabuleiro
        
        
        Parameter
        ---------------------
        size: int
            it's the input of the user that will be the size of the board
        """
        self.size = size
        self.tiles = [' '] * (size * size)

    def print_tabuleiro(self):
        """
        This method is prints the board by the size that has been passed.              
        """
        for i in range(0, len(self.tiles), self.size):
            print(" | ".join(self.tiles[i:i + self.size]))
            if i < len(self.tiles) - self.size:
                print("-" * (4 * self.size - 1))


class Pessoaj:
    """
    This class is the class of the player
    """
    def __init__(self, symbol):
        """
        This constructor method is responsible to save the symbol of the player
        
        Parameters
        -------------------
        
        symbol: str
            This is the representation of the symbol.
        """
        self.symbol = symbol


def main():
    while True:
        try:
            simbolo1 = input('Digite o valor do símbolo do primeiro jogador: ')
            if len(simbolo1) != 1:
                print('O símbolo do jogador deve ser único.')
                continue  # Go back to the beginning of the loop

            p1 = Pessoaj(simbolo1)

            simbolo2 = input('Digite o valor do símbolo do segundo jogador: ')
            if len(simbolo2) != 1:
                print('O símbolo do jogador deve ser único.')
                continue  # Go back to the beginning of the loop

            p2 = Pessoaj(simbolo2)

            tamanho_do_tabuleiro = int(input('Digite o tamanho do tabuleiro (mínimo 3): '))
            if tamanho_do_tabuleiro < 3:
                print('O tamanho do tabuleiro deve ser no mínimo 3.')
                continue  # Go back to the beginning

            meu_tab = Tabuleiro(tamanho_do_tabuleiro)
            meu_jogo = Game(meu_tab, p1, p2)
            meu_jogo.jogar()
            saida = input("Digite sair se quiser fechar o jogo: ") 
            if saida == 'sair':
                break  # Get out of the loop

        except ValueError as ve:
            print(f'Ocorreu um erro: {ve}')
        except Exception as e:
            print(f'Ocorreu um erro: {e}')


if __name__ == '__main__':
    main()
