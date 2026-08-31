#!/usr/bin/env python

import logging
import time
from simple_pid import PID

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%H:%M:%S')
log = logging.getLogger('water_boiler')


class WaterBoiler:
    """
    Simple simulation of a water boiler which can heat up water
    and where the heat dissipates slowly over time
    """

    def __init__(self):
        self.water_temp = 20

    def update(self, boiler_power, dt):
        if boiler_power > 0:
            # Boiler can only produce heat, not cold
            self.water_temp += 1 * boiler_power * dt

        # Some heat dissipation
        self.water_temp -= 0.02 * dt
        return self.water_temp


if __name__ == '__main__':
    boiler = WaterBoiler()
    water_temp = boiler.water_temp

    pid = PID(5, 0.01, 0.1, setpoint=water_temp)
    pid.output_limits = (0, 100)

    start_time = time.time()
    last_time = start_time
    last_log_time = start_time

    log.info("开始烧水，初始温度: %.2f °C", water_temp)

    while time.time() - start_time < 10:
        current_time = time.time()
        dt = current_time - last_time

        power = pid(water_temp)
        water_temp = boiler.update(power, dt)

        if current_time - start_time > 1:
            pid.setpoint = 100

        # 每隔 0.5 秒打印一次日志，体现控制过程
        if current_time - last_log_time >= 0.5:
            log.info(
                "t=%5.2fs | 目标: %6.2f °C | 当前: %6.2f °C | 功率: %5.1f%%",
                current_time - start_time,
                pid.setpoint,
                water_temp,
                power,
            )
            last_log_time = current_time

        last_time = current_time

    log.info("烧水结束，最终温度: %.2f °C", water_temp)
