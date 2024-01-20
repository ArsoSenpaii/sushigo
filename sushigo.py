import random
import math

card_type = {"Tempura":14, "Sashimi":14, "Dumbling":14, "1xMaki Roll":6, "2xMaki Roll":12, 
             "3xMaki Roll":8, "Salmon Nigiri":10, "Squid Nigiri":5, "Egg Nigiri":5, 
             "Pudding":10, "Wasabi":6, "Chopsticks":4,"Soya Sauce": 4}
card_list = [];
total_round = 3
total_turn = 8
total_user = 4

class Card:
    def __init__(self, type, id):
        self.id = id
        self.type = type;
    def __str__(self):
        return f"{self.type}({self.id})"

class User:
    def __init__(self, user_name, user_id):
        self.user_name = user_name
        self.user_id = user_id
        self.points = [0,0,0]
        self.total_point = 0
        self.user_drawn_cards = [[] for _ in range(3)]
        self.inventory = [[] for _ in range(3)]
    def __str__(self):
        return f"{self.user_name}({self.user_id}) - Points: {self.total_point}"

User1 = User("player",0)
User2 = User("bot1",1)
User3 = User("bot2",2)
User4 = User("bot3",3)

users = [User1,User2,User3,User4]

def throw_randomly(rounds):
    for user in users:
        drawn_card = random.choice(user.user_drawn_cards[rounds])
        user.user_drawn_cards[rounds].remove(drawn_card)
        user.inventory[rounds].append(drawn_card)
        
        
def deep_copy(list1, list2):
    for element in list2:
        list1.append(element)
    
def swap_the_cards(rounds):
    temp = []
    deep_copy(temp, users[3].user_drawn_cards[rounds])
    users[3].user_drawn_cards[rounds] = []
    deep_copy(users[3].user_drawn_cards[rounds], users[2].user_drawn_cards[rounds])
    users[2].user_drawn_cards[rounds] = []
    deep_copy(users[2].user_drawn_cards[rounds], users[1].user_drawn_cards[rounds])
    users[1].user_drawn_cards[rounds] = []
    deep_copy(users[1].user_drawn_cards[rounds], users[0].user_drawn_cards[rounds])
    users[0].user_drawn_cards[rounds] = []
    deep_copy(users[0].user_drawn_cards[rounds], temp)
    
def calculate_points():
    for i in range(3):
        soya_sauce_calculator(i)
        maki_roll_calculator(i)
        dumbling_calculator(i)
        sashimi_calculator(i)
        tempura_calculator(i)
        wasabi_nigiri_calculator(i)
    for user in users:
        user.total_point = sum(user.points)
    pudding_calculator()
    
def soya_sauce_calculator(rounds):
    color_counts = []
    have_soya_sauce = []
    for user in users:
        color_count = 0
        has_soya_sauce = 0

        maki_count = 1
        nigiri_count = 1

        type_counts = {"Tempura": 1, "Sashimi": 1, "Dumbling": 1,
                    "Maki Roll": maki_count, "Salmon Nigiri": nigiri_count,
                    "Squid Nigiri": nigiri_count, "Egg Nigiri": nigiri_count, "Wasabi": 1,
                    "Pudding": 1, "Chopsticks": 1, "Soya Sauce": 1}

        for element in user.inventory[rounds]:
            if element.type in type_counts:
                color_count += type_counts[element.type]
                type_counts[element.type] = 0

                if element.type == "Soya Sauce":
                    has_soya_sauce += 1

                if "Maki" in element.type:
                    maki_count = 0
                elif "Nigiri" in element.type:
                    nigiri_count = 0

        color_counts.append(color_count)
        have_soya_sauce.append(has_soya_sauce)
    players_with_max_color = 0
    for i in range(4):
        if (color_counts[i] == max(color_counts)) and (have_soya_sauce[i] == 0):
            return
    for i in range(4):
        if (color_counts[i] == max(color_counts)) and (have_soya_sauce[i] >= 1):
            players_with_max_color+=1
    for i in range(4):
        if (color_counts[i] == max(color_counts)) and (have_soya_sauce[i] >= 1):
            users[i].points[rounds] += math.floor(4/players_with_max_color)           
    
def maki_roll_calculator(rounds):
    maki_roll_counts = []
    for user in users:
        maki_roll_count = 0
        for element in user.inventory[rounds]:
            if element.type == "1xMaki Roll":
                maki_roll_count+=1       
            if element.type == "2xMaki Roll":
                maki_roll_count+=2   
            if element.type == "3xMaki Roll":
                maki_roll_count+=3
        maki_roll_counts.append(maki_roll_count)
                    
    players_with_max_maki_roll = 0
    players_with_2nd_max_maki_roll = 0
    max_maki_roll_count = max(maki_roll_counts)
    
    for i in range(4):
        if maki_roll_counts[i] == max_maki_roll_count:
            players_with_max_maki_roll+=1
            maki_roll_counts[i] = -1
    for i in range(4):
        if maki_roll_counts[i] == max(maki_roll_counts):
            players_with_2nd_max_maki_roll+=1
            maki_roll_counts[i] = -2
    if players_with_max_maki_roll == 1:
         for i in range(4):    
            if maki_roll_counts[i] == -1:
                users[i].points[rounds] += 6
            elif maki_roll_counts[i] == -2:
                users[i].points[rounds] += math.floor(3/players_with_2nd_max_maki_roll) 
    else:
        for i in range(4):    
            if maki_roll_counts[i] == -1:
                users[i].points[rounds] += math.floor(6/players_with_max_maki_roll)
    
def dumbling_calculator(rounds):
    for user in users:
        dumbling_count = 0
        for element in user.inventory[rounds]:
            if element.type == "Dumbling":
                dumbling_count+=1
        if dumbling_count == 1:
            user.points[rounds] += 1
        if dumbling_count == 2:
            user.points[rounds] += 3
        if dumbling_count == 3:
            user.points[rounds] += 6
        if dumbling_count == 4:
            user.points[rounds] += 10
        if dumbling_count >= 5:
            user.points[rounds] += 15
    
def sashimi_calculator(rounds):
    for user in users:
        sashimi_count = 0
        for element in user.inventory[rounds]:
            if element.type == "Sashimi":
                sashimi_count+=1
        user.points[rounds] += 10*math.floor(sashimi_count/3)      

def tempura_calculator(rounds):
    for user in users:
        tempura_count = 0
        for element in user.inventory[rounds]:
            if element.type == "Tempura":
                tempura_count+=1
        user.points[rounds] += 5*math.floor(tempura_count/2) 
    
def wasabi_nigiri_calculator(rounds):
    for user in users:
        for i in range(8):
            point = 0
            if user.inventory[rounds][i].type == "Salmon Nigiri":
                point = 2
            if user.inventory[rounds][i].type == "Squid Nigiri":
                point = 3
            if user.inventory[rounds][i].type == "Egg Nigiri":
                point = 1
            if i>0 and user.inventory[rounds][i].type == "Wasabi":
                point*=3
            user.points[rounds] += point

def pudding_calculator():
    pudding_counts = []
    for user in users:
        pudding_count = 0
        for inventory in user.inventory:
            for card in inventory:
                if card.type == "Pudding":
                    pudding_count+=1
        pudding_counts.append(pudding_count)
        
    players_with_max_pudding = 0
    players_with_min_pudding = 0
    
    for i in range(4):
        if pudding_counts[i] == max(pudding_counts):
            players_with_max_pudding += 1
        if pudding_counts[i] == min(pudding_counts):
            players_with_min_pudding += 1
    for i in range(4):
        if pudding_counts[i] == max(pudding_counts):
            users[i].total_point += math.floor(6/players_with_max_pudding)
        if pudding_counts[i] == min(pudding_counts):
            users[i].total_point -= math.floor(6/players_with_min_pudding)    

def reveal_the_winner():
    winners = {}
    points = [user.total_point for user in users]
    
    for user in users:
        if user.total_point == max(points):
            winners[user.user_name] = user.total_point
    for name, points in winners.items():
        print(f'{name}: {points} points')

for card, count in card_type.items():
    for i in range(count):
        card_list.append(Card(card, i))
        
random.seed()
drawn_cards = random.sample(card_list, total_turn*total_round*total_user)

for user in users:
    for i in range(total_round):
        for _ in range(total_turn):
            user.user_drawn_cards[i].append(drawn_cards.pop(0))

rounds = 0
while (rounds < total_round):
    turn = 0
    while (turn < total_turn):
        throw_randomly(rounds)
        swap_the_cards(rounds)
        turn+=1
    rounds+=1

calculate_points()   
reveal_the_winner()