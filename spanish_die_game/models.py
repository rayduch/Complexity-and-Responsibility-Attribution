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

# For Questionnaire

    age = models.IntegerField(
        verbose_name='Edad',
        min=13, max=125)

    gender = models.IntegerField(
        choices=[1,'Hombre', 2, 'Mujer', 3, 'Otro'],
        verbose_name='Sexo',
        widget=widgets.RadioSelect)

    ideology = models.IntegerField(
        choices=[0 , '0. Izquierda', 1, '1.', 2, '2. ', 3, '3.', 4, '4. ', 5, '5.', 6, '6. ', 7, '7.', 8, '8. ', 9, '9.', 10, '10. Derecha '],
        verbose_name='En política se habla normalmente de "izquierda" y "derecha". En una escala donde "0" es la "izquierda" y 10 la "derecha", ¿dónde se ubicaría?',
        widget=widgets.RadioSelectHorizontal)

    trust = models.IntegerField(
        choices=[1,'Se puede confiar en la mayoría de las personas', 2, 'Uno nunca es lo suficientemente cuidadoso en el trato con los demá'],
        verbose_name=' En general, ¿diría que se puede confiar en la mayoría de las personas o que uno nunca es lo suficientemente cuidadoso en el trato con los demás?',
        widget=widgets.RadioSelect)

    occupation = models.IntegerField(
        choices=[1,'Estudiante', 2, 'Trabajador', 3, 'Otro'],
        verbose_name='¿Cuál es su ocupación principal?',
        widget=widgets.RadioSelect)

    scholarship = models.IntegerField(
        choices=[1,'Sí', 2, 'No'],
        verbose_name='¿Es beneficiario de alguna beca?',
        widget=widgets.RadioSelect)
