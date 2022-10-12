"""
Author:
Nilusink
"""
import matplotlib.animation as anim
import matplotlib.pyplot as plt
import serial.tools.list_ports
import numpy as np
import serial
import time


MAX_EXPECTED_DISTANCE: float = 300  # in meters
DISTANCE_STORAGE_LENGTH: int = 10  # in seconds
PULSE_RESOLUTION: int = 1000  # just for visuals

MAX_PULSE_LENGTH: float = (2 * MAX_EXPECTED_DISTANCE) / 0.034


def main():
    ports = list(serial.tools.list_ports.comports())

    print("Available Ports:")
    print(*ports, sep="\n", end="\n\n")

    port = input("Port: ")

    # initialize graph
    fig = plt.figure(num="HC-SR04")
    dist = fig.add_subplot(2, 1, 1)
    wave = fig.add_subplot(2, 1, 2)

    # connect to to serial device
    arduino = serial.Serial(port, 9600)

    start_time = time.time()
    d_times: list[float] = []
    distances: list[float] = []
    all_distances: list[float] = []

    def update(*_a):
        nonlocal d_times, distances

        arduino.flushInput()

        duration_microseconds = distance = 0
        while True:
            try:
                line = arduino.readline().decode().rstrip("\r\n")

            except UnicodeError:
                plt.plot(d_times, distances)
                continue

            try:
                duration_microseconds, distance = line.split("\t")
                duration_microseconds = float(duration_microseconds)
                distance = float(distance)

                if distance > MAX_EXPECTED_DISTANCE:
                    distance = 0
                    duration_microseconds = 0

                break

            except ValueError:
                continue

        # append to data
        d_times.append(time.time() - start_time)
        all_distances.append(distance)
        distances.append(distance)

        # remove old values
        for i in range(len(d_times)):
            if (d_times[-1] - d_times[i]) > DISTANCE_STORAGE_LENGTH:
                d_times[i] = None
                distances[i] = None

        d_times = list(filter(lambda x: x is not None, d_times))
        distances = list(filter(lambda x: x is not None, distances))

        # generate pulse data
        p_xs: list[float] = list(np.linspace(0, MAX_PULSE_LENGTH, PULSE_RESOLUTION) * 10**-3)
        p_ys: list[float] = []

        pulse_points = int(PULSE_RESOLUTION * (duration_microseconds / MAX_PULSE_LENGTH))
        non_pulse_points = PULSE_RESOLUTION - pulse_points

        p_ys += [1] * pulse_points
        p_ys += [0] * non_pulse_points

        # append pre- and post-points
        n_e = 4
        p_xs = list(
            np.linspace(-MAX_PULSE_LENGTH / 4, 0, n_e) * 10**-3
        ) + p_xs + list(
            np.linspace(MAX_PULSE_LENGTH, MAX_PULSE_LENGTH * 1.25, n_e) * 10**-3
        )
        p_ys = [0.0] * n_e + p_ys + [0.0] * n_e

        if len(p_ys) != len(p_xs):
            p_xs = p_ys = []

        # distance plot
        lines.set_xdata(d_times)
        lines.set_ydata(distances)
        dist.relim()
        dist.autoscale_view()
        # m_d = max(list(filter(lambda e: e is not np.inf, all_distances)))
        m_d = 150
        dist.set_ylim(0, m_d if m_d else 1)

        # pulse plot
        w_lines.set_xdata(p_xs)
        w_lines.set_ydata(p_ys)
        wave.relim()
        wave.autoscale_view()
        wave.set_ylim(-0.5, 1.5)

        # expand
        plt.tight_layout()

    # configure graph
    dist.set_title("Distanz")
    dist.set_ylabel("Distanz in cm")
    dist.set_xlabel("t in s")
    dist.grid()
    lines, = dist.plot([], [])

    wave.set_title("Pulslänge")
    wave.set_ylabel("True / Fale")
    wave.set_xlabel("t in ms")
    wave.grid()
    w_lines, = wave.plot([], [])

    _a = anim.FuncAnimation(fig, update, repeat=True, interval=0)
    plt.show()


if __name__ == '__main__':
    main()
