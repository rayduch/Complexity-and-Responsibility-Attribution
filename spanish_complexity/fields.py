from otree.api import models, widgets

LOTTERYCHOICES1st = ((False, 'No pagar el costo'), (True, 'Pagar el costo'))
LOTTERYCHOICES3d = ((False, 'No'), (True, 'Yes'))

class LotteryField(models.BooleanField):
    description = "field for lotter choices and guesses"

    def __init__(self, third_person=False,*args, **kwargs):
        kwargs['widget'] = widgets.RadioSelectHorizontal
        if third_person:
            kwargs['choices'] = LOTTERYCHOICES3d
        else:
            kwargs['choices'] = LOTTERYCHOICES1st
        super().__init__(*args, **kwargs)
