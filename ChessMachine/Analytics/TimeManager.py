
from .analyze_board import analyze_board
import numpy as np

class TimeManager:

    def __init__(self, is_white: bool, game_time: int, additional_time: int):
        self.is_white = is_white
        self.game_time = game_time
        self.additional_time = additional_time

        self.estimated_rounds = 40.0

    def schedlue_time(self, my_time_left, enemy_time_left, board, rounds_passed):

        wh_value, bl_value, total_count = analyze_board(board)

        # mnożnik przewagi

        adv_scaled = (wh_value - bl_value) / (wh_value + bl_value)

        if(self.is_white):
            m_advantage = 1.0 - np.sign(adv_scaled) * abs(adv_scaled) ** 0.6
        else:
            m_advantage = 1.0 + np.sign(adv_scaled) * abs(adv_scaled) ** 0.6

        m_advantage = np.clip(m_advantage, 0.2, 2.0)

        # mnożnik czasu
        time_adv = (my_time_left - enemy_time_left) / (my_time_left + enemy_time_left)

        m_time = 1.0 + np.sign(time_adv) * abs(time_adv)** 0.4
        m_time = np.clip(m_time, 0.5, 2.0)

        # a tu mamy modyfikację ilości rund
        phase = (total_count - 5) / 32
        deadline = my_time_left / self.game_time
        pressure = phase - deadline

        self.estimated_rounds += pressure * 2

        if (self.estimated_rounds - rounds_passed < 5) and (total_count > 7):
            self.estimated_rounds += 2
        elif (self.estimated_rounds - rounds_passed < 1) and (total_count > 4):
            self.estimated_rounds += 3



        schedlued_time = my_time_left / (int(self.estimated_rounds) - rounds_passed)

        return schedlued_time * 0.6 + schedlued_time * 0.4 * m_advantage * m_time
