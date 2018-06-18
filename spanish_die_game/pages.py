from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
from otree.forms.widgets import _CurrencyInput

class Instructions(Page):
    def vars_for_template(self):
        return {'curname':_CurrencyInput.CURRENCY_SYMBOL}


class DiceRolling(Page):
    form_model = 'player'
    form_fields = ['dice', 'report']

    def before_next_page(self):
        self.player.set_payoff()

class FinalResults(Page):
    def vars_for_template(self):
        print("final results: ", self.session.config['real_world_currency_per_point'])
        return {
            'modules1_chosen_round': self.participant.vars[self.player.session_id]['part1_chosenRounds'][0],
            'modules2_chosen_round': self.participant.vars[self.player.session_id]['part1_chosenRounds'][1],
            'modules1_payoff': self.participant.vars[self.player.session_id]['part1_payoff'][0],
            'modules2_payoff': self.participant.vars[self.player.session_id]['part1_payoff'][1],
            'modules3_payoff': self.participant.vars[self.player.session_id]['part2_payoff'],
            'modules4_payoff': self.participant.vars[self.player.session_id]['part3_payoff'],
            'show_up_fee': 2000,
            'total_payoff': int((self.participant.vars[self.player.session_id]['part1_payoff'][0] +
                            self.participant.vars[self.player.session_id]['part1_payoff'][1] +
                            self.participant.vars[self.player.session_id]['part3_payoff']) * 2 +
                            self.participant.vars[self.player.session_id]['part2_payoff'] +
                            2000)
        }


class DiceRollingResults(Page):
    ...

class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['age', 'gender','ideology','trust', 'occupation', 'scholarship']


page_sequence = [
    Instructions,
    DiceRolling,
    DiceRollingResults,
    Questionnaire,
    FinalResults
]
