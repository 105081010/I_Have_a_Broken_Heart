# -*- coding: utf-8 -*-
import random
from agent import Agent
from game import Game
from card import Card
import card


class MyAgent(Agent):
    def play(self, cards_you_have, cards_played, heart_broken, info):
        cards = Game.get_legal_moves(cards_you_have, cards_played, heart_broken)
        return random.choice(cards)
    
    #return largest card in hand
    def pass_cards(self, cards): #cards 是三小
        print (cards)
        desired_passed_card=[]
        card_you_can_pass=3
        a=0
        spade_number=[]
        dimond_number=[]
        flower_number=[]
        
        for card in cards: #有多少個花色在手排中 
            if card.suit == '♠':
                spade_number.append(card)
            if card.suit == '♦':
                dimond_number.append(card)
            if card.suit == '♣':
                flower_number.append(card)
        
        print ('flower_number:',flower_number, 'spade_number:',spade_number, 'dimond:',dimond_number)
        if len(spade_number)<=5: #手排中的黑陶小於等於五張時 又 有黑桃大排時，就要pass掉
            copy_spade_number = spade_number[:]
            for card in copy_spade_number:
                if card.number==12:
                    desired_passed_card.append(card)
                    cards.remove(card)
                    card_you_can_pass-=1
                if  card.number==13:
                    desired_passed_card.append(card)
                    cards.remove(card)
                    card_you_can_pass-=1
                if  card.number==1:
                    desired_passed_card.append(card)
                    cards.remove(card)
                    card_you_can_pass-=1
            print('黑陶部分:',desired_passed_card, card_you_can_pass)

        #如果菱形梅花都很少 選擇總點數比較少的那個            
        if len(flower_number) <= (card_you_can_pass+1) and len(dimond_number)<=(card_you_can_pass):
            print('進入數字大小比較')
            total_flower_number=0
            total_dimond_number=0
            for card in flower_number:
                if card.number==1:total_flower_number+=13
                else: total_flower_number+=card.number
    
            for card in dimond_number:
                if card.number==1:total_dimond_number+=13
                else: total_dimond_number+=card.number
            if  (total_flower_number/len(flower_number))>(total_dimond_number/len(dimond_number)):
                a=1
                print('梅花獲得pass權')
            else:
                a=2
                print('菱形獲得pass權')            

        if len(flower_number) <= (card_you_can_pass+1)and a!=2:#送掉梅花排
            copy_flower_number = flower_number[:]
            for card in copy_flower_number:
                desired_passed_card.append(card)
                cards.remove(card)
                card_you_can_pass-=1
                if card_you_can_pass==0:break
                
            print('梅花部分',desired_passed_card,card_you_can_pass)
                    
        if len(dimond_number)<=(card_you_can_pass)and a!=1:#送掉菱形排
            copy_dimond_number = dimond_number[:]
            for card in copy_dimond_number:
                desired_passed_card.append(card)
                cards.remove(card)
                card_you_can_pass-=1
                if card_you_can_pass==0:break
            
            print('菱形部分',desired_passed_card, card_you_can_pass)
            
        if True:#最後就找大牌
            largest = sorted(cards, key=lambda c: int(c.number==1)*13+c.number,reverse=True)[:3]
            desired_passed_card = desired_passed_card + largest[:card_you_can_pass]
            print('找大牌' ,desired_passed_card)
        
        print('final',desired_passed_card )
        return desired_passed_card
                
                
                
                
                
  
    def memorize(self, cards):
        
        self.memory = {suit:
                       [Card(suit, number)
                       for number in card._number
                       if Card(suit, number) not in cards]
                       for suit in card._suit}
        
    def remove_played_cards(self, cards_lists, cards_played):
        for c in cards_played:
            self.memory[c.suit].remove(c)
        
        for cards_list in cards_lists[::-1]:
            for idx, c in cards_list[::-1]:
                if c in self.mycard:
                    return
                self.memory[c.suit].remove(c)
        
        
    def compute_card_rank(self, cards):
        self.card_rank = {}
        cards_suit = {suit:[] for suit in card._suit}
        for c in cards:
            cards_suit[c.suit].append(c)
        
        for suit in card._suit:
            cards_suit[suit].extend(self.memory[suit])
            cards_suit[suit].sort()
        
        rank = {suit:0 for suit in card._suit}
        for suit in card._suit:
            start = True
            mycard = False
            for c in cards_suit[suit]:
                if start:
                    if c in cards:
                        self.card_rank[c] = rank[suit]
                        mycard = True
                    else:
                        self.card_rank[c] = rank[suit]
                        rank[suit] += 1
                        mycard = False
                    start = False
                
                if c in cards:
                    mycard = True
                    self.card_rank[c] = rank[suit]
                else:
                    if mycard:
                        rank[suit] += 1
                    self.card_rank[c] = rank[suit]
                    mycard = False
                    rank[suit] += 1
                    
    
    def get_good_moves(self, cards_you_have, cards_played, heart_broken, legal_moves):
        cards_suit = {suit:[] for suit in card._suit}
        for c in legal_moves:
            cards_suit[c.suit].append(c)
        if cards_played:
            main_suit = cards_played[0].suit
            max_card = max([c for c in cards_played if c.suit == main_suit])
            score = sum(c.point for c in cards_played)
            
            if score > 0:
                #avoid getting points
                smaller = [c for c in legal_moves if c.suit!=main_suit or c<max_card]
                if smaller:
                    return random.choice(self.largest_cards(smaller))
                
                #you will get points anyway, so play the biggest card in your hand
                if main_suit == '♠' and Card('♠', 12) in self.memory['♠']:
                    candidates = [c for c in legal_moves if c.suit != '♠' or (c.number != 1 and c.number !=13)]
                    if not candidates:
                        candidates = legal_moves[:]
                else:
                    candidates = legal_moves[:]
                    
                return random.choice(self.largest_cards(candidates))
            elif main_suit == '♠':
                # playing any card you want, but don't play ♠13,♠1
                if Card('♠', 12) in self.memory['♠'] and len(cards_played) != 3:
                    candidates = [c for c in legal_moves if c.suit != '♠' or (c.number != 1 and c.number !=13)]
                    if not candidates:
                        candidates = legal_moves[:]

                    return random.choice(self.largest_cards(candidates))
                elif Card('♠', 12) in legal_moves:
                    if max_card > Card('♠', 12):
                        return Card('♠', 12)
                    else:
                        candidates = [c for c in legal_moves if c.suit != '♠' or c.number != 12]
                        if not candidates:
                            return Card('♠', 12)
                                  
                        return random.choice(self.largest_cards(candidates))
                else:
                    return random.choice(self.largest_cards(legal_moves))
            else:
                if Card('♠', 12) in legal_moves:
                    return Card('♠', 12)
                return random.choice(self.largest_cards(legal_moves))
        else:
                                  
            #playing cards that has a chance to give others
            candidates = []
            for suit, cards in cards_suit.items():
                if not cards:
                    continue
                min_card = min(cards, key=lambda c: self.card_rank[c])
                min_card_rank = self.card_rank[min_card]
                smallest_rank = [c for c in cards if self.card_rank[c] == min_card_rank]
                if len(smallest_rank) == len(cards):
                    continue
                candidates.extend([c for c in cards if self.card_rank[c] == min_card_rank])
            
            if candidates:
                return random.choice(candidates)
            
            return random.choice(legal_moves)
                                  
    def largest_cards(self, cards):
        max_card = max(cards, key=lambda c: self.card_rank[c])
        max_card_rank = self.card_rank[max_card]
        largest_rank = [c for c in cards if self.card_rank[c] == max_card_rank]

        return largest_rank
