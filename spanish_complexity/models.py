from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
from .fields import LotteryField
import random
import numpy as np
import math
# from .perfect_matching import PerfectMatch as pm
from django.conf import settings

author = 'Philipp Chapkovski, Danlin Chen'

doc = """
R.Duch, D. Landa project on die_game
"""




def get_practice_rounds(num_practice, num_first_part):
    first_set = list(range(1, num_practice + 1))
    second_set = list(range(num_first_part + 1, num_first_part + num_practice + 1))
    return first_set + second_set


def get_last_n_rounds(n, num_first_part, num_rounds):
    first_set = list(range(num_first_part - n + 1, num_first_part + 1))
    second_set = list(range(num_rounds - n + 1, num_rounds + 1))
    return first_set + second_set


class Constants(BaseConstants):


    name_in_url = 'spanish_complexity'
    players_per_group = 2
    # how many practice rounds we have
    num_practice = 0
    assert players_per_group == 2, 'Number of players should be 2 for correct role assignemnt'
    num_rounds = 8
    num_first_part = 5
    num_participants = settings.SESSION_CONFIGS[0].get('num_demo_participants')# number of participants
    ####perfect matching####
    cons1 = np.zeros([num_first_part - 2, num_participants], dtype=int)
    var = np.full([num_first_part - 2, math.floor(num_participants/2) ], -1)
    Domain = np.zeros([num_participants, num_participants], dtype=int)
    Assignment = np.zeros([num_first_part - 2, math.floor(num_participants/2), 2], dtype=int)
    ########################
    num_second_part = num_rounds - num_first_part
    # when the second decision (guess) about p1 decision is shown
    num_second_dec = 1 # run at least 7 rounds per respondent
    assert num_first_part - 2 < num_rounds, 'First set of decisions should be less then total number of rounds'
    assert 2 < num_first_part - 2 and 2 < num_second_part, 'training rounds number should be ' \
                                                                             'strictly less than total number of rounds'
    assert num_first_part - 2 - num_practice >= num_second_dec and num_second_part - num_practice >= num_second_dec
    practice_rounds = get_practice_rounds(num_practice, num_first_part)
    p2_second_decision_rounds = get_last_n_rounds(num_second_dec, num_first_part, num_rounds)
    pweights = [5, 5]
    tot_prop = sum(pweights)
    prob = round(pweights[0] / sum(pweights), 2)  # probability of success if P1 invests
    p1endowment = 300
    lotterycost = 150
    retention_prize = 900
    guess_prize = 140
    success_prize = 500
    roles_dict = {
        'P1': 'Player 1',
        'P2': 'Player 2',
    }
    RETAININGCHOICES = (
        (0, 'NUNCA recompensar al Jugador 1'),
        (1, 'Recompensar al Jugador si y sólo sí el Resultado es Éxito en AMBAS Tareas'),
        (2, 'Recompensar al jugador 1 si y sólo sí el Resultado es Éxito en al menos una Tarea  (eso es,  O en la Tarea '
            '1, O en la Tarea 2, O en AMBAS Tareas  1 y 2)'),
        (3, 'Recompensar al Jugador 1 si y sólo sí el Resultado es Éxito en sólo una Tarea (Tarea 1 O Tarea 2)'),
        (4, 'SIEMPRE Recompensar al Jugador 1'),
    )




class Subsession(BaseSubsession):
    def set_random(self):
        self.group_randomly()
        # print("subsession: ", self.round_number, "mtx: ", self.get_group_matrix())

    def set_mtx(self):
        # if self.round_number == 2:
        # PM = pm(Constants.Assignment, Constants.Domain, Constants.var, Constants.cons1, Constants.num_participants,Constants.num_first_part - 2)
        # pm.do_shuffle(PM)
        # print(Constants.Assignment)
        # print( "Assginemtn: ", Constants.Assignment)
        if self.round_number <= Constants.num_first_part and self.round_number != 1:
            round_mtx = []
            print ("round number: ", self.round_number)
            players = self.get_players()
            p1List = [i for i in range(0, Constants.num_participants, 2)]
            p2List = [i for i in range(1, Constants.num_participants, 2)]
            p2ListA = p2List[0:self.round_number - 3]
            p2List = p2List[self.round_number - 3: len(p2List)] + p2ListA
            for pair in range(0, math.floor(Constants.num_participants / 2)):
                p1 = p1List[pair]
                p2 = p2List[pair]
                round_mtx.append([players[p1], players[p2]])
            print("round: ", self.round_number, "group matrix: ", round_mtx)
            self.set_group_matrix(round_mtx)


    def creating_session(self):
        # print("round: ", self.round_number)
        if self.round_number == 1:
            self.group_randomly() # practice usage
            for p in self.session.get_participants():
                pround1 = random.randint(1 + 2, Constants.num_first_part) # 2 is practice number
                pround2 = random.randint(Constants.num_first_part + 1, Constants.num_rounds)
                p.vars['paying_rounds'] = [pround1, pround2]
                # print('Subsession pround1: ',pround1, 'pround2: ',pround2)
        if self.round_number == 2:
            self.group_randomly()
        else:
            self.set_mtx()


LOTTERYOUTCOMES = ((True, 'Éxito'), (False, 'Fracaso'),)

P1DecisionSTRING = """
¿Quiere pagar el costo en la Tarea {task}? El costo es {lotterycost}, Si paga, las probabilidades de Éxito en la 
tarea son de {success_p} de {totp}."""


def get_decision_string(task):
    return P1DecisionSTRING.format(
        lotterycost=c(Constants.lotterycost),
        success_p=Constants.pweights[0],
        totp=sum(Constants.pweights),
        task=task
    )


class Group(BaseGroup):
    task1decision = LotteryField(doc='lottery decision of P1 - task 1',
                                 verbose_name=get_decision_string(1),
                                 )
    task2decision = LotteryField(doc='lottery decision of P1 - task 2',
                                 verbose_name=get_decision_string(2),
                                 )
    # in outcome we use choices just for get_foo_display method later on
    task1outcome = models.BooleanField(doc=' outcome of task 1',
                                       choices=LOTTERYOUTCOMES)
    task2outcome = models.BooleanField(doc='outcome of task 2',
                                       choices=LOTTERYOUTCOMES)
    task1guess = LotteryField(doc='P2 guess of lottery decision of P1 - task 1',
                              verbose_name='El Jugador 1 pagará el costo de la Tarea 1',
                              third_person=True,
                              )
    task2guess = LotteryField(doc='P2 guess of lottery decision of P1 - task 2',
                              verbose_name='El Jugador 1 pagará el costo de la Tarea 2',
                              third_person=True,

                              )
    retaining = models.IntegerField(doc='retaining/firing decision of P2 regarding P1',
                                    choices=Constants.RETAININGCHOICES,
                                    verbose_name='Elija una Regla para Recompensar o No Recompensar al Jugador 1',
                                    widget=widgets.RadioSelect)

    # print('task1decision', task1decision)

    def get_retention_decision(self):
        return {
            0: False,
            1: self.task1outcome + self.task2outcome == 2,
            2: self.task1outcome + self.task2outcome >= 1,
            3: self.task1outcome + self.task2outcome == 1,
            4: True,
        }[self.retaining]

    def get_decision(self):
        return Constants.RETAININGCHOICES[self.get_retention_decision()][1]

    def get_guess1(self):
        if self.task1guess:
            if self.task1decision:
                return 'Correcto'
            else:
                return 'Incorrecto'
        else:
            if self.task1decision:
                return 'Incorrecto'
            else:
                return 'Correcto'

    def get_guess2(self):
        if self.task2guess:
            if self.task2decision:
                return 'Correcto'
            else:
                return 'Incorrecto'
        else:
            if self.task2decision:
                return 'Incorrecto'
            else:
                return 'Correcto'

    def set_outcome(self):
        self.task1outcome = self.task1decision * random.choices(LOTTERYOUTCOMES, weights=Constants.pweights)[0][0]
        self.task2outcome = self.task2decision * random.choices(LOTTERYOUTCOMES, weights=Constants.pweights)[0][0]

        #if self.round_number in [1,2]:
        #    self.task1outcome = 0
        #    self.task2outcome = 0

    def get_sum_guess_prize(self):
        return ((self.task1decision == self.task1guess) + (
            self.task2decision == self.task2guess)) * Constants.guess_prize

    def set_payoff(self):
        self.set_outcome()
        P1 = self.get_player_by_role('P1')
        P2 = self.get_player_by_role('P2')
        # print(self.task1guess, self.task1guess, self.task1decision, self.task1outcome)
        sum_success = (self.task1outcome + self.task2outcome) * Constants.success_prize
        sum_guess = self.get_sum_guess_prize()
        P2.payoff = sum_success + sum_guess
        P1.payoff = (Constants.p1endowment - (self.task1decision + self.task2decision) * Constants.lotterycost +
                     self.get_retention_decision() * Constants.retention_prize)

        # workaround to save variables in CSV
        P1.task1 = self.task1decision
        P1.task2 = self.task2decision
        P1.task1outcome2 = self.task1outcome
        P1.task2outcome2 = self.task2outcome
        P2.pretaining = self.retaining
        P2.task1guess2 = self.task1guess
        P2.task2guess2 = self.task2guess


        if self.round_number in [1,2]:
            P1.payoff = 0
            P2.payoff = 0

    def set_final_payoff(self):
        assert self.round_number == Constants.num_rounds, 'You should not call this method before the final round'
        for p in self.get_players():
            paying_rounds = p.participant.vars['paying_rounds']
            for r in p.in_all_rounds():
                r.temp_payoff = r.payoff
                if r.round_number not in paying_rounds:
                    r.payoff = 0


class Player(BasePlayer):
    """we defining role simply as: at the first part of the study odd players are P1s, and at the
    second half: even players become P1s"""
    temp_payoff = models.CurrencyField(doc='to store all interim payoffs')

    def role(self):
        roles = list(Constants.roles_dict.keys())
        if bool(self.round_number <= Constants.num_first_part) ^ bool(self.id_in_group % 2 == 0):
            return roles[0]
        else:
            return roles[1]

    def get_role_name(self):
        return Constants.roles_dict[self.role()]

    def get_another_role(self):
        roles = list(Constants.roles_dict.keys())
        another_role = list((set(roles) - set([self.role()])))[0]
        return Constants.roles_dict[another_role]

    #To copy variable
    task1 = models.IntegerField()
    task2 = models.IntegerField()
    task1outcome2 = models.IntegerField()
    task2outcome2 = models.IntegerField()
    task1guess2 = models.IntegerField()
    task2guess2 = models.IntegerField()
    pretaining = models.IntegerField()