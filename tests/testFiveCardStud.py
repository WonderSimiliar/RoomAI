#!/bin/python
from roomai.fivecardstud import FiveCardStudEnv
from roomai.fivecardstud import FiveCardStudPokerCard
from roomai.fivecardstud import FiveCardStudAction
from roomai.fivecardstud import FiveCardStudRandomPlayer
import unittest
import roomai
import roomai.fivecardstud

class FiveCardStudTester(unittest.TestCase):
    def test(self):
        env = FiveCardStudEnv();
        env.init()

    def testCase(self):

        cards   =[FiveCardStudPokerCard("3_Spade"), FiveCardStudPokerCard("4_Spade"),FiveCardStudPokerCard("5_Spade"),FiveCardStudPokerCard("6_Spade")]
        pattern = FiveCardStudEnv.fourcards2pattern(cards)
        assert(pattern[0] =="Straight_SameSuit")

        cards = [FiveCardStudPokerCard("3_Spade"), FiveCardStudPokerCard("4_Spade"), FiveCardStudPokerCard("5_Spade"),
                 FiveCardStudPokerCard("6_Spade")]


    def testEnv(self):
        env = FiveCardStudEnv();
        env.chips = [1000,1000,1000]
        infos, pu, pes, pr = env.init()

        turn = pu.turn
        assert(pes[turn].available_actions is not None)
        available_actions = pes[turn].available_actions
        assert("Call_0" not in available_actions)
        assert("Fold_0" in available_actions)
        assert("Check_0"  in available_actions)

        showhand_act_key = ""
        for act_str in available_actions:
            if "Showhand" in act_str:
                showhand_act_key = act_str

        env.forward(FiveCardStudAction(showhand_act_key))
        env.forward(FiveCardStudAction(showhand_act_key))
        infos, pu, pe, pr = env.forward(FiveCardStudAction(showhand_act_key))

        assert(env.public_state.is_terminal == True)
        print pu.scores
        print pu.floor_bet
        assert(max(pu.scores) == 2000/pu.floor_bet)
        assert(min(pu.scores) == -1000/pu.floor_bet)
        print infos[0].public_state.round
        print infos[0].person_state.fifth_hand_card.get_key()

    def testRandomPlayer(self):

        for i in xrange(100):
            players = [roomai.fivecardstud.FiveCardStudRandomPlayer() for i in xrange(3)]
            env     = roomai.fivecardstud.FiveCardStudEnv()
            env.num_players = 3
            env.chips       = [1000,1000,1000]

            infos,public_state,_,_ = env.init()
            for i in xrange(len(players)):
                players[i].receive_info(infos[i])

            while public_state.is_terminal == False:
                turn = public_state.turn
                action = players[turn].take_action()

                infos,public_state,_,_ = env.forward(action)
                for i in xrange(len(players)):
                    players[i].receive_info(infos[i])

        for i in xrange(100):
            players = [roomai.fivecardstud.FiveCardStudRandomPlayer() for i in xrange(2)]
            env     = roomai.fivecardstud.FiveCardStudEnv()
            env.num_players = 2
            env.chips       = [1000,1000]

            infos,public_state,_,_ = env.init()
            for i in xrange(len(players)):
                players[i].receive_info(infos[i])

            while public_state.is_terminal == False:
                turn = public_state.turn
                action = players[turn].take_action()

                infos,public_state,_,_ = env.forward(action)
                for i in xrange(len(players)):
                    players[i].receive_info(infos[i])


    def testCompete(self):
        env     = FiveCardStudEnv()
        players = [FiveCardStudRandomPlayer() for i in xrange(5)]
        scores  = FiveCardStudEnv.compete(env, players)
        print scores
        assert(abs(sum(scores)) < 1e-9 )

if __name__ == "__main__":
    env = FiveCardStudEnv()
    players = [FiveCardStudRandomPlayer() for i in xrange(5)]
    scores = FiveCardStudEnv.compete(env, players)