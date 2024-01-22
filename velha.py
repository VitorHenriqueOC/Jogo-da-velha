import os
class Game:
    def __init__(self, tabuleiro, p1, p2) -> None:
        self.tabuleiro = tabuleiro
        self.jogador = [p1, p2]
        self.turno = 0

    def player_round(self, jogador_atual):
        print(f"Sua vez: {jogador_atual.symbol}")

    def jogar(self):
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
        if not (0 <= move < len(self.tabuleiro.tiles) and self.tabuleiro.tiles[move] == " "):
            raise InvalidMoveError('Movimento inválido. Tente novamente.')

    def check_vitoria(self, jogador_symbol):
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
        if all(tiles[i * size + i] == jogador_symbol for i in range(size)):
            return jogador_symbol
        if all(tiles[i * size + (size - 1 - i)] == jogador_symbol for i in range(size)):
            return jogador_symbol

        return False

    def record_result(self, vencedor):
        file_path = os.path.join(os.getcwd(), 'scoreboard.txt')
        with open(file_path, 'a+') as file:
            file.write(f'Player: {vencedor.symbol}, Score: 1\n')
        print("Current working directory:", os.getcwd())

        
        
        

    def game_over(self, jogador_symbol):
        print(f'Acabou! Jogador com símbolo {jogador_symbol} ganhou!')
        self.record_result(self.jogador[self.turno])  


class InvalidMoveError(Exception):
    pass


class Tabuleiro:
    def __init__(self, size) -> None:
        self.size = size
        self.tiles = [' '] * (size * size)

    def print_tabuleiro(self):
        for i in range(0, len(self.tiles), self.size):
            print(" | ".join(self.tiles[i:i + self.size]))
            if i < len(self.tiles) - self.size:
                print("-" * (4 * self.size - 1))


class Pessoaj:
    def __init__(self, symbol):
        self.symbol = symbol


def main():
    while True:
        try:
            simbolo1 = input('Digite o valor do símbolo do primeiro jogador: ')
            if len(simbolo1) != 1:
                print('O símbolo do jogador deve ser único.')
                continue  # Voltar ao início do loop

            p1 = Pessoaj(simbolo1)

            simbolo2 = input('Digite o valor do símbolo do segundo jogador: ')
            if len(simbolo2) != 1:
                print('O símbolo do jogador deve ser único.')
                continue  # Voltar ao início do loop

            p2 = Pessoaj(simbolo2)

            tamanho_do_tabuleiro = int(input('Digite o tamanho do tabuleiro (mínimo 3): '))
            if tamanho_do_tabuleiro < 3:
                print('O tamanho do tabuleiro deve ser no mínimo 3.')
                continue  # Voltar ao início do loop

            meu_tab = Tabuleiro(tamanho_do_tabuleiro)
            meu_jogo = Game(meu_tab, p1, p2)
            meu_jogo.jogar()
            break  # Sair do loop em caso de sucesso

        except ValueError as ve:
            print(f'Ocorreu um erro: {ve}')
        except Exception as e:
            print(f'Ocorreu um erro: {e}')


if __name__ == '__main__':
    main()
