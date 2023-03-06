from PIL import ImageTk, Image
import numpy as np
from itertools import permutations
from hand_eval import leduc_eval
from cards import Card
from state import State
import pickle
import tkinter as tk
from tkinter import ttk
import functools


with open('trained_models/cfr_train3.pickle', 'rb') as f:
    node_map, action_map = pickle.load(f)

num_players = 2
num_rounds = 2
num_cards = num_players+1


def get_image_name(card):
    card_name_dict = {
        'A': 'Ace',
        '2': 'Two',
        '3': 'Three',
        '4': 'Four',
        '5': 'Five',
        '6': 'Six',
        '7': 'Seven',
        '8': 'Eight',
        '9': 'Nine',
        '10': 'Ten',
        'J': 'Jack',
        'Q': 'Queen',
        'K': 'King',
        'spade': 'Spades',
        'clubs': 'Clubs',
        'hearts': 'Hearts',
        'diamond': 'Diamonds'}

    return f"{card_name_dict[card.value[0]]} of {card_name_dict[card.value[1]]}.png"


# Default cards in the deck
cards = [Card('J', 'spade'), Card('Q', 'spade'), Card('K', 'spade'),
         Card('J', 'diamond'), Card('Q', 'diamond'), Card('K', 'diamond')]
# print(get_image_name(cards[2]))

# Shuffle and initialize state with cards
card_combinations = [list(t) for t in set(permutations(cards, num_cards))]
random_int = np.random.choice(len(card_combinations))

card = card_combinations[random_int]
ss = State(num_players, num_rounds, leduc_eval)
ss.start_state(card)


def create_background(width=1000, height=750):
    # Create a window
    root = tk.Tk()
    root.title("Poker Table")

    # Create a canvas to draw the poker table

    canvas = tk.Canvas(root, width=width, height=height, bg="#006600")
    canvas.pack()

    deltax = (width-800)/2
    deltay = (height-600)/2

    # Draw the poker table
    canvas.create_rectangle(50+deltax, 50+deltay, 750+deltax,
                            550+deltay, fill="#003300", width=0)
    canvas.create_rectangle(100+deltax, 100+deltay, 700 +
                            deltax, 500+deltay, fill="#006600", width=0)
    canvas.create_oval(275+deltax, 275+deltay, 525+deltax,
                       425+deltay, fill="#006600", width=0)
    canvas.create_line(275+deltax, 100+deltay, 275+deltax,
                       500+deltay, fill="#FFFFFF", width=2)
    canvas.create_line(525+deltax, 100+deltay, 525+deltax,
                       500+deltay, fill="#FFFFFF", width=2)

    # Add some text to the table
    canvas.create_text(400+deltax, 75+deltay, text="Poker Table",
                       font=("Arial", 30), fill="#FFFFFF")
    # canvas.create_text(275, 525, text="Dealer", font=("Arial", 20), fill="#FFFFFF")
    # canvas.create_text(525, 525, text="Player", font=("Arial", 20), fill="#FFFFFF")

    canvas.create_text(400+deltax, 525+deltay, text="Dealer", font=(
        "Arial", 20), fill="#FFFFFF")
    canvas.create_text(725+deltax, 300+deltay, text="AI player", font=(
        "Arial", 20), fill="#FFFFFF", angle=90)
    canvas.create_text(75+deltax, 300+deltay, text="Human Player", font=(
        "Arial", 20), fill="#FFFFFF", angle=270)

    # Run the window
    return root, canvas


def get_ai_id(root, canvas):
    def get_input(answer):
        var.set(answer)

    # Create a style for the buttons
    style = ttk.Style()
    style.configure("TButton", padding=0, relief="flat",
                    background="#ccc", foreground="#333", font=("Arial", 12))

    # Create a label to display the question
    ql = question_label = tk.Label(
        root, text="Who should play first ?", font=("Arial", 14))
    question_label.pack(padx=10, side='left')

    # Create variables for the buttons
    var = tk.IntVar()
    var.set(-1)

    # Create buttons for the user's input
    button0 = ttk.Button(root, text="AI",
                         command=lambda: get_input(0), style="TButton")
    button1 = ttk.Button(root, text="Human",
                         command=lambda: get_input(1), style="TButton")
    button0.pack(side='left', pady=10, padx=50)
    button1.pack(side='left', pady=10, padx=50)

    root.wait_variable(var)

    ql.destroy()
    button1.destroy()
    button0.destroy()

    # var.wait_variable()
    print("var:", var.get())
    return var.get()


def get_action(root, canvas, actions):
    def get_input(answer):
        var.set(answer)

    # Create a style for the buttons
    style = ttk.Style()
    style.configure("TButton", padding=0, relief="flat",
                    background="#ccc", foreground="#333", font=("Arial", 12))

    # Create a label to display the question
    question_label = tk.Label(
        root, text="Choose an action: ", font=("Arial", 14))
    question_label.pack(padx=10, side='left')

    # Create variables for the buttons
    var = tk.StringVar()
    var.set('-1')

    buttons = [None for _ in range(len(actions))]
    for i, a in enumerate(actions):
     # Create buttons for the user's input

        buttons[i] = ttk.Button(root, text=a,
                                command=functools.partial(get_input, a), style="TButton")

        buttons[i].pack(side='left', pady=10, padx=50)

    root.wait_variable(var)

    for b in buttons:
        b.destroy()
    question_label.destroy()

    # var.wait_variable()

    return var.get()


pot_ids = []


def show_pot(root, canvas, pot_total, bets, width, height):
    global pot_ids
    if len(pot_ids) > 0:
        for ids in pot_ids:
            canvas.delete(ids)
        pot_ids = []

    deltax = (width-800)/2
    deltay = (height-600)/2

    canvas.create_oval(300+deltax, 100+deltay, 500+deltax,
                       200+deltay, fill="#700000", width=8)

    # Display that it is a pot
    id = canvas.create_text(400+deltax, 120+deltay, text="Pot", font=(
        "Arial", 15), fill="#FFFFFF")
    pot_ids.append(id)
    # Display total amount in the pot
    id = canvas.create_text(400+deltax, 150+deltay, text="Total:{0}".format(pot_total), font=(
        "Arial", 15), fill="#FFFFFF")
    pot_ids.append(id)

    # Individual bets
    id = canvas.create_text(670+deltax, 450+deltay, text="Bet:{0}".format(bets[0]), font=(
        "Arial", 15), fill="#FFFFFF", angle=90)
    pot_ids.append(id)
    id = canvas.create_text(130+deltax, 150+deltay, text="Bet:{0}".format(bets[1]), font=(
        "Arial", 15), fill="#FFFFFF", angle=270)
    pot_ids.append(id)

    return root, canvas


def ai_is_thiking(root, canvas, width, height):
    '''
    Delays certin time before AI makes an action
    '''
    deltax = (width-800)/2
    deltay = (height-600)/2

    # Display 'AI_is_thinking'
    id = canvas.create_text(700+deltax, 50+deltay, text="AI is thinking...", font=(
        "Arial", 15), fill="#FFFFFF")

    return root, canvas, id


def show_utility(root, canvas, utility, width, height):
    '''
    Shows utility of player
    '''
    deltax = (width-800)/2
    deltay = (height-600)/2

    # Display 'action taken by ai'
    canvas.create_text(400+deltax, 575+deltay, text="Your Gain(/Loss) : {0}".format(utility), font=(
        "Arial", 20), fill="#FFFFFF")

    return root, canvas


ai_action_id = -10


def ai_action(root, canvas, action, width, height):
    global ai_action_id
    if ai_action != -10:
        canvas.delete(ai_action_id)

    deltax = (width-800)/2
    deltay = (height-600)/2

    # Display 'action taken by ai'
    ai_action_id = canvas.create_text(700+deltax, 50+deltay, text="Action : {0}".format(action), font=(
        "Arial", 15), fill="#FFFFFF")

    return root, canvas


def show_card(root, canvas, hc, ac, cc, h, a, c):
    '''
    Shows card
    '''

    global tk_image1, tk_image2, tk_image3
    if h:
        image1 = Image.open("images/" + hc)
        image1 = image1.resize((55, 85), Image.LANCZOS).transpose(
            Image.ROTATE_90).transpose(Image.ROTATE_90).transpose(Image.ROTATE_90)
        tk_image1 = ImageTk.PhotoImage(image1)
        canvas.create_image(100+(85/2), 300, anchor='nw', image=tk_image1, )

    else:
        image1 = Image.open("images/default.png")
        image1 = image1.resize((55, 85), Image.LANCZOS).transpose(
            Image.ROTATE_90).transpose(Image.ROTATE_90).transpose(Image.ROTATE_90)
        tk_image1 = ImageTk.PhotoImage(image1)
        canvas.create_image(100+(85/2), 300, anchor='nw', image=tk_image1)

    if a:
        image2 = Image.open("images/"+ac)
        image2 = image2.resize(
            (55, 85), Image.LANCZOS).transpose(Image.ROTATE_90)
        tk_image2 = ImageTk.PhotoImage(image2)
        canvas.create_image(712.5-(85/2), 300, anchor='nw', image=tk_image2)

    else:
        image2 = Image.open("images/default.png")
        image2 = image2.resize(
            (55, 85), Image.LANCZOS).transpose(Image.ROTATE_90)
        tk_image2 = ImageTk.PhotoImage(image2)
        canvas.create_image(712.5-(85/2), 300, anchor='nw', image=tk_image2)

    if c:
        image3 = Image.open("images/"+cc)
        image3 = image3.resize((55, 85), Image.LANCZOS)
        tk_image3 = ImageTk.PhotoImage(image3)
        canvas.create_image(400, 500-(85/2), anchor='nw', image=tk_image3)
    else:
        image3 = Image.open("images/default.png")
        image3 = image3.resize((55, 85), Image.LANCZOS)
        tk_image3 = ImageTk.PhotoImage(image3)
        canvas.create_image(400, 500-(85/2), anchor='nw', image=tk_image3)

    return root, canvas


def play(root, canvas, width, height):
    # Choose the player number for ai
    # Define a function to get input from the user

    ai_id = get_ai_id(root, canvas)

    # Calculate human id from ai_id
    human_id = int(not ai_id)

    # Show pot amount
    if human_id == 0:
        root, canvas = show_pot(root, canvas, ss.pot_total(), [
            ss.players[1].total, ss.players[0].total], width, height)
    else:
        root, canvas = show_pot(root, canvas, ss.pot_total(), [
            ss.players[0].total, ss.players[1].total], width, height)

    # print("Amount in Pot:{0} [{1},{2}]".format(
    #     ss.pot_total(), ss.players[0].total, ss.players[1].total))

    # Show your card
    human_card_name = get_image_name(ss.get_player(human_id).card)
    cc_name = get_image_name(ss.state['cc'])
    # print(human_card_name)
    ai_card_name = get_image_name(ss.get_player(ai_id).card)
    root, canvas = show_card(root, canvas, human_card_name,
                             ai_card_name, cc_name, h=True, a=False, c=False)

    # print("Your card: {0}".format(ss.get_player(human_id).card))

    v = 0
    while(not ss.is_terminal()):
        # Get the turn and round
        turn = ss.state['turn']
        r = ss.state['round']

        # Reveal community card once when reaching round 1
        if r == 1 and v == 0:
            v = 1
            root, canvas = show_card(root, canvas, human_card_name,
                                     ai_card_name, cc_name, h=True, a=False, c=True)

        # If the turn is for ai to play
        if turn == ai_id:

            # Get current info set and use strategy according to it
            info_set = ss.info_set(ai_id)
            node = node_map[turn][info_set]
            strategy = node.avg_strategy()

            # Find the action according to categorical distribution over action given by strategy
            random_action = np.random.choice(
                list(strategy.keys()), p=list(strategy.values()))

            root, canvas = ai_action(
                root, canvas, random_action, height, width)

            # Act the chosen action
            ss.succesor_state(random_action)

            # Show pot
            if human_id == 0:
                root, canvas = show_pot(root, canvas, ss.pot_total(), [
                    ss.players[1].total, ss.players[0].total], width, height)
            else:
                root, canvas = show_pot(root, canvas, ss.pot_total(), [
                    ss.players[0].total, ss.players[1].total], width, height)

            # # Show pot amount in console
            # print("Amount in Pot:{0} [{1},{2}]".format(
            #     ss.pot_total(), ss.players[0].total, ss.players[1].total))

        # If the turn is for human to play
        else:
            # Get valid action and act according to it
            valid_actions = ss.actions()
            action = str(get_action(root, canvas, valid_actions))
            ss.succesor_state(action)

            # Show pot amount
            if human_id == 0:
                root, canvas = show_pot(root, canvas, ss.pot_total(), [
                    ss.players[1].total, ss.players[0].total], width, height)
            else:
                root, canvas = show_pot(root, canvas, ss.pot_total(), [
                    ss.players[0].total, ss.players[1].total], width, height)

            # print("Amount in Pot:{0} [{1},{2}]".format(
            #     ss.pot_total(), ss.players[0].total, ss.players[1].total))

    # Finally after reaching terminal stage show AI card and your score
    else:
        root, canvas = show_card(root, canvas, human_card_name,
                                 ai_card_name, cc_name, h=True, a=True, c=True)

        # Show your loss or gain
        utility = ss.utility()
        show_utility(root, canvas, int(utility[human_id]), width, height)


if __name__ == '__main__':
    window, canvas = create_background(900, 675)
    play(window, canvas, 900, 675)

    window.mainloop()
