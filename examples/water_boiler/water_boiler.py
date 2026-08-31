#!/usr/bin/env python

import logging
import time

import click
import numpy as np
from simple_pid import PID

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s', datefmt='%H:%M:%S')
log = logging.getLogger('water_boiler')


class WaterBoiler:
    """
    Simple simulation of a water boiler which can heat up water
    and where the heat dissipates slowly over time.
    The measured temperature includes Gaussian sensor noise.
    """

    def __init__(self, initial_temp=20.0, noise_std=0.1, seed=None):
        self.water_temp = initial_temp
        self.noise_std = noise_std
        self.rng = np.random.default_rng(seed)

    def update(self, boiler_power, dt):
        if boiler_power > 0:
            # Boiler can only produce heat, not cold
            self.water_temp += 1 * boiler_power * dt

        # Some heat dissipation
        self.water_temp -= 0.02 * dt
        return self.measure()

    def measure(self):
        # 真实测量值带有传感器噪声
        return self.water_temp + self.rng.normal(0.0, self.noise_std)


@click.command()
@click.option('--target', default=100.0, show_default=True, help='目标温度 (°C)')
@click.option('--duration', default=10.0, show_default=True, help='模拟时长 (s)')
@click.option('--log-interval', default=0.5, show_default=True, help='日志打印间隔 (s)')
@click.option('--kp', default=5.0, show_default=True, help='PID 比例增益')
@click.option('--ki', default=0.01, show_default=True, help='PID 积分增益')
@click.option('--kd', default=0.1, show_default=True, help='PID 微分增益')
@click.option('--noise', default=0.1, show_default=True, help='传感器噪声标准差 (°C)')
@click.option('--seed', default=None, type=int, help='随机种子，固定后结果可复现')
def main(target, duration, log_interval, kp, ki, kd, noise, seed):
    boiler = WaterBoiler(noise_std=noise, seed=seed)
    water_temp = boiler.measure()

    pid = PID(kp, ki, kd, setpoint=water_temp)
    pid.output_limits = (0, 100)

    start_time = time.time()
    last_time = start_time
    last_log_time = 0.0

    # 记录数据，结束后用 numpy 计算控制性能指标
    times, measurements = [], []

    log.info("开始烧水，初始温度: %.2f °C，目标温度: %.1f °C", water_temp, target)

    while time.time() - start_time < duration:
        current_time = time.time()
        dt = current_time - last_time

        power = pid(water_temp)
        water_temp = boiler.update(power, dt)

        elapsed = current_time - start_time

        if elapsed > 1:
            pid.setpoint = target

        # 每隔一段时间打印一次日志，体现控制过程
        if elapsed - last_log_time >= log_interval:
            log.info(
                "t=%5.2fs | 目标: %6.2f °C | 当前: %6.2f °C | 功率: %5.1f%%",
                elapsed,
                pid.setpoint,
                water_temp,
                power,
            )
            last_log_time = elapsed

        last_time = current_time
        times.append(elapsed)
        measurements.append(water_temp)

    # 计算控制性能指标（只看设定点改变之后的阶段）
    times = np.array(times)
    measurements = np.array(measurements)
    after = times > 1.0

    rise_time = overshoot = steady_error = float('nan')
    if after.any():
        t = times[after] - 1.0
        y = measurements[after]

        # 上升时间：温度首次达到目标 90% 所需时间
        reached = y >= 0.9 * target
        if reached.any():
            rise_time = float(t[np.argmax(reached)])

        # 最大超调量
        overshoot = max(0.0, float(np.max(y) - target))

        # 稳态误差：最后 2 秒平均温度与目标的偏差
        steady_window = min(2.0, t[-1])
        steady = y[t >= t[-1] - steady_window]
        steady_error = float(np.mean(steady) - target)

    log.info("烧水结束，最终温度: %.2f °C", water_temp)
    log.info(
        "性能指标 | 上升时间: %.2f s | 超调量: %.2f °C | 稳态误差: %+.2f °C",
        rise_time,
        overshoot,
        steady_error,
    )


if __name__ == '__main__':
    main()
