import random
import os


class Cards(object):
    cards = (
    '2_pik', '2_kier', '2_trefl', '2_karo', '3_pik', '3_kier', '3_trefl', '3_karo', '4_pik', '4_kier', '4_trefl',
    '4_karo', '5_pik', '5_kier', '5_trefl', '5_karo', '6_pik', '6_kier', '6_trefl', '6_karo', '7_pik', '7_kier',
    '7_trefl', '7_karo','8_pik', '8_kier', '8_trefl', '8_karo', '9_pik', '9_kier', '9_trefl', '9_karo', '10_pik',
    '10_kier', '10_trefl', '10_karo', 'J_pik', 'J_kier', 'J_trefl', 'J_karo', 'D_pik', 'D_kier', 'D_trefl', 'D_karo',
    'K_pik', 'K_kier', 'K_trefl', 'K_karo', 'AS_pik', 'AS_kier', 'AS_trefl', 'AS_karo')

    def pick_card(self):
        return random.choice(self.cards)

    def pick_cards(self):
        return random.sample(self.cards, 2)


class Player(Cards):
    def __init__(self, bankroll=100, score=0, player_cards=[], bet=0):
        self.player_cards = player_cards
        self.score = score
        self.bankroll = bankroll
        self.bet = bet

    def count_score(self, used_card):
        self.score = 0
        for i in used_card:
            point = i.split('_')[0]
            if (point == 'J') or (point == 'D') or (point == 'K'):
                point = 10
            elif point == 'AS':
                point = 11
            self.score += int(point)
        return self.score

    def chceck_bankroll(self, result):
        if result == "YOU WON":
            self.bankroll = self.bankroll + self.bet
        elif result == "YOU LOST":
            self.bankroll = self.bankroll - self.bet
        return self.bankroll

    def player_result(self, ob, result='N'):
        ob.score = ob.count_score(ob.player_cards)
        if result != 'N':
            if ob.chceck_bankroll(result) <= 0:
                print("You are bankrupt. \nTry again")
                exit()
        return (
            "have {} and have {} score. You bet is {}$. Your bank roll is {} $".format(self.player_cards, self.score,
                                                                                       self.bet, self.bankroll)
            if self.bet != 0 else "have {} and have {} score.".format(self.player_cards, self.score))


def check_win(score_bob, score_croupier):
    if score_bob == 21 or score_croupier > 21 or score_bob > score_croupier and score_bob < 21:
        return "YOU WON"
    elif score_croupier == 21 or score_bob > 21 or score_bob < score_croupier:
        return "YOU LOST"
    elif score_bob == score_croupier:
        return "TIE"


def check_21(bob, croupier):
    if bob.score == 21:
        return ("Bob " + bob.player_result(bob) + " You WON")
    elif croupier.score == 21:
        return ("Croupier " + croupier.player_result(croupier) + " He WON")
    else:
        return 0


def next_pick_up(used_card, decision='N'):
    deck = Cards()
    deck_cards = list(deck.cards)
    for i in used_card:
        deck_cards.remove(i)
    if decision == 'H':
        next_cards = random.sample(deck_cards, 1)
    else:
        next_cards = random.sample(deck_cards, 2)
    return next_cards


def player_input():
    plin = input("Write H for Hit or S for Stand. Your choice: ").upper()

    if plin == 'H':
        return plin
    elif plin == 'S':
        return plin
    else:
        print("Invalid input. Enter H or S: ")
        player_input()


def play_again():
    plin = input("Do you wanna play again Y/N? Your choice: ").upper()
    if plin == 'Y':
        os.system('cls')
        return plin
    elif plin == 'N':
        print('Thanks for playing!')
        exit()
    else:
        print("Invalid input. Enter Y for yes or N for no: ")
        play_again()


def start_game(bob=Player()):
    if bob.score == 0:
        print("Welcome in Blackjack game. You have 100 $ and the bet is for 10 $. Have fun and good luck!\n\n")
    bob.bet = 10
    bob.player_cards = bob.pick_cards()
    bob.score = bob.count_score(bob.player_cards)

    croupier = Player()
    croupier.player_cards = next_pick_up(bob.player_cards)
    croupier.score = croupier.count_score(croupier.player_cards)

    test_21 = check_21(bob, croupier)
    if test_21:
        print(test_21)
        play_again()
    else:
        print("Bob", bob.player_result(bob))
        print("Croupier have {} and unsigned card ".format(croupier.player_cards[0]))
    play_game(bob, croupier)


def play_game(bob, croupier):
    plin = player_input()
    if plin == 'H':
        bob.player_cards += next_pick_up(bob.player_cards + croupier.player_cards, plin)
        print("Bob", bob.player_result(bob))
        play_game(bob, croupier) if bob.score <= 21 else print(check_win(bob.score, croupier.score),
                                                               "\nBob", bob.player_result(bob, check_win(bob.score,
                                                                                                         croupier.score)),
                                                               "\nCroupier", croupier.player_result(croupier))
    elif plin == 'S':
        if croupier.score <= 11:
            croupier.player_cards += next_pick_up(bob.player_cards + croupier.player_cards, 'H')
            croupier.count_score(croupier.player_cards)
        print(check_win(bob.score, croupier.score), "\nBob",
              bob.player_result(bob, check_win(bob.score, croupier.score)), "\nCroupier",
              croupier.player_result(croupier))

    if play_again() == 'Y':
        start_game(bob)




start_game()