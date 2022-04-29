import random
from enum import IntEnum

settings = "y"

y = 1

class Action(IntEnum):
    Rock = 0
    Paper = 1
    Scissors = 2


victories = {
    Action.Scissors: [Action.Paper],
    Action.Paper: [Action.Rock],
    Action.Rock: [Action.Scissors]
}


def get_user_selection():
    choices = [f"{action.name}[{action.value}]" for action in Action]
    choices_str = ", ".join(choices)
    selection = int(input(f"Вы выбираете ({choices_str}): "))
    action = Action(selection)
    return action


def get_computer_selection():
    selection = random.randint(0, len(Action) - 1)
    action = Action(selection)
    return action


def determine_winner(user_action, computer_action):
    if settings == "y":
        computer_action = user_action + 1
        if computer_action == 3:
            computer_action = 0
        y = computer_action
    action = Action(computer_action)
    computer_action = action
    defeats = victories[user_action]
    if user_action == computer_action:
        print(f"Оба игрока выбрали {user_action.name}. Это ничья!")
    elif computer_action in defeats:
        print(f"{user_action.name} бьет {computer_action.name}! Вы победили!")
    else:
        print(f"{computer_action.name} бьет {user_action.name}! Вы проиграли. :C")
    return y