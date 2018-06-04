from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)

author = 'Your name here'

doc = """
Your app description
"""




class Constants(BaseConstants):
    name_in_url = 'spanish_die_game'
    players_per_group = None
    num_rounds = 1
    report_coef = 100


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    dice = models.IntegerField(min=1, max=6,
                               verbose_name='Por favor informe el número del dado')
    report = models.StringField(verbose_name='Informe el dado del sistema', blank=True)

    def set_payoff(self):
        self.payoff = Constants.report_coef * self.dice
        self.participant.vars[self.session_id]['part3_payoff'] = self.payoff / 1.0
