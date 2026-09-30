"""Numerical calculations for ENAE 601 Homework 02."""

from pathlib import Path

import numpy as np
from scipy.optimize import brentq


MU_EARTH = 398600.0  # km^3/s^2
R_EARTH = 6378.0  # km
OUTPUT_DIR = Path(__file__).resolve().parents[1] / "outputs" / "text"


def heading(problem: str) -> None:
    """Print the heading used to separate each problem's output."""
    print(f"\n------\n {problem}\n------")


def write_output(problem: str, lines: list[str]) -> None:
    """Print and save a problem's text output."""
    output = "\n".join(lines) + "\n"
    print(output, end="")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUTPUT_DIR / f"s{problem}.txt").write_text(output, encoding="utf-8")


def eccentric_anomaly(mean_anomaly: float, eccentricity: float) -> float:
    """Solve elliptic Kepler's equation for E in [0, 2 pi]."""
    return brentq(
        lambda anomaly: anomaly - eccentricity * np.sin(anomaly) - mean_anomaly,
        0.0,
        2.0 * np.pi,
    )


def hyperbolic_anomaly(mean_anomaly: float, eccentricity: float) -> float:
    """Solve hyperbolic Kepler's equation; works for either sign of M."""
    extent = max(1.0, np.arcsinh(abs(mean_anomaly) / eccentricity) + 1.0)
    return brentq(
        lambda anomaly: eccentricity * np.sinh(anomaly) - anomaly - mean_anomaly,
        -extent,
        extent,
    )


def hyperbolic_mean_from_true(true_anomaly: float, eccentricity: float) -> float:
    """Return signed hyperbolic mean anomaly from signed true anomaly."""
    factor = np.sqrt((eccentricity - 1.0) / (eccentricity + 1.0))
    anomaly = 2.0 * np.arctanh(factor * np.tan(true_anomaly / 2.0))
    return eccentricity * np.sinh(anomaly) - anomaly


def problem_02() -> None:
    """Curtis 3.5: flight time from periapsis to the minor axis."""
    heading("p02")
    eccentric_anomaly = np.pi / 2.0
    constant_term = eccentric_anomaly / (2.0 * np.pi)
    eccentricity_coefficient = -np.sin(eccentric_anomaly) / (2.0 * np.pi)
    write_output(
        "02",
        [
            f"E_B = {eccentric_anomaly:.12f} rad = pi/2",
            "t/T = (E_B - e sin(E_B))/(2 pi)",
            f"t/T = {constant_term:.12f} {eccentricity_coefficient:+.12f} e",
            "exact result: t/T = 1/4 - e/(2 pi)",
        ],
    )


def problem_03() -> None:
    """Curtis 3.6: flight time to a true anomaly of 90 degrees."""
    heading("p03")
    eccentricity = 0.3
    true_anomaly = np.pi / 2.0
    eccentric_anomaly_value = np.arccos(
        (eccentricity + np.cos(true_anomaly))
        / (1.0 + eccentricity * np.cos(true_anomaly))
    )
    time_period_ratio = (
        eccentric_anomaly_value - eccentricity * np.sin(eccentric_anomaly_value)
    ) / (2.0 * np.pi)
    write_output(
        "03",
        [
            f"e = {eccentricity:.12f}",
            f"theta_B = {np.degrees(true_anomaly):.12f} deg",
            f"E_B = {eccentric_anomaly_value:.12f} rad "
            f"= {np.degrees(eccentric_anomaly_value):.12f} deg",
            f"t/T = {time_period_ratio:.12f}",
        ],
    )


def problem_04() -> None:
    """Curtis 3.8: duration above 400 km altitude."""
    heading("p04")
    radius_perigee = R_EARTH + 200.0
    radius_apogee = R_EARTH + 600.0
    semimajor_axis = (radius_perigee + radius_apogee) / 2.0
    eccentricity = (radius_apogee - radius_perigee) / (radius_apogee + radius_perigee)
    mean_motion = np.sqrt(MU_EARTH / semimajor_axis**3)
    eccentric_anomaly_crossing = np.arccos(
        (1.0 - (R_EARTH + 400.0) / semimajor_axis) / eccentricity
    )
    mean_anomaly_crossing = eccentric_anomaly_crossing - eccentricity * np.sin(
        eccentric_anomaly_crossing
    )
    duration = (2.0 * np.pi - 2.0 * mean_anomaly_crossing) / mean_motion
    write_output(
        "04",
        [
            f"a = {semimajor_axis:.6f} km",
            f"e = {eccentricity:.9f}",
            f"time above 400 km = {duration:.6f} s = {duration / 60.0:.6f} min",
        ],
    )


def problem_05() -> None:
    """Curtis 3.9: swept anomaly and area over a time interval."""
    heading("p05")
    radius_perigee, radius_apogee = 7000.0, 10000.0
    semimajor_axis = (radius_perigee + radius_apogee) / 2.0
    eccentricity = (radius_apogee - radius_perigee) / (radius_apogee + radius_perigee)
    mean_motion = np.sqrt(MU_EARTH / semimajor_axis**3)
    times = np.array([0.5, 1.5]) * 3600.0
    mean_anomalies = mean_motion * times
    eccentric_anomalies = np.array(
        [
            eccentric_anomaly(mean_anomaly, eccentricity)
            for mean_anomaly in mean_anomalies
        ]
    )
    true_anomalies = 2.0 * np.arctan2(
        np.sqrt(1.0 + eccentricity) * np.sin(eccentric_anomalies / 2.0),
        np.sqrt(1.0 - eccentricity) * np.cos(eccentric_anomalies / 2.0),
    )
    delta_true_anomaly = true_anomalies[1] - true_anomalies[0]
    angular_momentum = np.sqrt(MU_EARTH * semimajor_axis * (1.0 - eccentricity**2))
    swept_area = 0.5 * angular_momentum * (times[1] - times[0])
    common = [
        f"a = {semimajor_axis:.6f} km; e = {eccentricity:.9f}",
        f"theta(0.5 h) = {np.degrees(true_anomalies[0]):.6f} deg",
        f"theta(1.5 h) = {np.degrees(true_anomalies[1]):.6f} deg",
    ]
    write_output(
        "05a",
        common + [f"delta theta = {np.degrees(delta_true_anomaly):.6f} deg"],
    )
    write_output(
        "05b",
        [
            f"swept area = {swept_area:.6f} km^2",
        ],
    )


def problem_06() -> None:
    """Curtis 3.10: state after 10 hours on an elliptic orbit."""
    heading("p06")
    period = 14.0 * 3600.0
    radius_perigee = 10000.0
    semimajor_axis = np.cbrt(MU_EARTH * (period / (2.0 * np.pi)) ** 2)
    eccentricity = 1.0 - radius_perigee / semimajor_axis
    mean_motion = 2.0 * np.pi / period
    mean_anomaly = mean_motion * 10.0 * 3600.0
    anomaly = eccentric_anomaly(mean_anomaly, eccentricity)
    radius = semimajor_axis * (1.0 - eccentricity * np.cos(anomaly))
    speed = np.sqrt(MU_EARTH * (2.0 / radius - 1.0 / semimajor_axis))
    radial_speed = (
        mean_motion
        * semimajor_axis
        * eccentricity
        * np.sin(anomaly)
        / (1.0 - eccentricity * np.cos(anomaly))
    )
    common = [
        f"a = {semimajor_axis:.6f} km; e = {eccentricity:.9f}",
        f"E(10 h) = {np.degrees(anomaly):.6f} deg",
    ]
    write_output("06a", common + [f"radius = {radius:.6f} km"])
    write_output("06b", [f"speed = {speed:.9f} km/s"])
    write_output(
        "06c",
        [
            f"radial velocity = {radial_speed:.9f} km/s",
        ],
    )


def problem_07() -> None:
    """Curtis 3.15: parabolic time of flight and 36-hour radius."""
    heading("p07")
    radius_perigee = 6600.0
    semilatus_rectum = 2.0 * radius_perigee
    barker_scale = 0.5 * np.sqrt(semilatus_rectum**3 / MU_EARTH)
    time_minus_90_to_plus_90 = 2.0 * barker_scale * (1.0 + 1.0 / 3.0)
    barker_rhs = 36.0 * 3600.0 / barker_scale
    parabolic_anomaly = brentq(
        lambda anomaly: anomaly + anomaly**3 / 3.0 - barker_rhs,
        0.0,
        np.cbrt(3.0 * barker_rhs) + 1.0,
    )
    radius_36_hours = radius_perigee * (1.0 + parabolic_anomaly**2)
    write_output(
        "07a",
        [
            f"time from -90 deg to +90 deg = {time_minus_90_to_plus_90:.6f} s "
            f"= {time_minus_90_to_plus_90 / 60.0:.6f} min",
        ],
    )
    write_output(
        "07b",
        [
            f"D(36 h) = {parabolic_anomaly:.9f}",
            f"radius at 36 h = {radius_36_hours:.6f} km",
        ],
    )


def problem_08() -> None:
    """Curtis 3.16: hyperbolic time of flight and 24-hour radius."""
    heading("p08")
    radius_perigee = 6600.0
    eccentricity = 2.0 * 1.2**2 - 1.0
    semimajor_axis_magnitude = radius_perigee / (eccentricity - 1.0)
    mean_motion = np.sqrt(MU_EARTH / semimajor_axis_magnitude**3)
    mean_at_90 = hyperbolic_mean_from_true(np.pi / 2.0, eccentricity)
    coast_time = 2.0 * mean_at_90 / mean_motion
    mean_anomaly_24_hours = mean_motion * 24.0 * 3600.0
    anomaly_24_hours = hyperbolic_anomaly(mean_anomaly_24_hours, eccentricity)
    radius_24_hours = semimajor_axis_magnitude * (
        eccentricity * np.cosh(anomaly_24_hours) - 1.0
    )
    common = [f"e = {eccentricity:.9f}; |a| = {semimajor_axis_magnitude:.6f} km"]
    write_output(
        "08a",
        common
        + [
            f"time from -90 deg to +90 deg = {coast_time:.6f} s "
            f"= {coast_time / 60.0:.6f} min",
        ],
    )
    write_output(
        "08b",
        [
            f"radius at 24 h = {radius_24_hours:.6f} km",
        ],
    )


def problem_09() -> None:
    """Curtis 3.17: propagate from a specified inbound speed to 5 p.m."""
    heading("p09")
    radius_perigee = R_EARTH + 200.0
    eccentricity = 2.0 * 1.1**2 - 1.0
    semimajor_axis_magnitude = radius_perigee / (eccentricity - 1.0)
    mean_motion = np.sqrt(MU_EARTH / semimajor_axis_magnitude**3)
    speed_initial = 8.0
    radius_initial = 2.0 / (
        speed_initial**2 / MU_EARTH - 1.0 / semimajor_axis_magnitude
    )
    anomaly_magnitude = np.arccosh(
        (radius_initial / semimajor_axis_magnitude + 1.0) / eccentricity
    )
    anomaly_initial = -anomaly_magnitude
    mean_initial = eccentricity * np.sinh(anomaly_initial) - anomaly_initial
    mean_final = mean_initial + mean_motion * 7.0 * 3600.0
    anomaly_final = hyperbolic_anomaly(mean_final, eccentricity)
    radius_final = semimajor_axis_magnitude * (
        eccentricity * np.cosh(anomaly_final) - 1.0
    )
    write_output(
        "09",
        [
            f"e = {eccentricity:.9f}; |a| = {semimajor_axis_magnitude:.6f} km",
            f"radius at 10 a.m. = {radius_initial:.6f} km",
            f"time from 10 a.m. to perigee = {-mean_initial / mean_motion / 3600.0:.9f} h",
            f"radius at 5 p.m. = {radius_final:.6f} km",
            f"altitude at 5 p.m. = {radius_final - R_EARTH:.6f} km",
        ],
    )


def problem_10() -> None:
    """Curtis 3.18: impact test and time from sighting to impact."""
    heading("p10")
    radius_initial = R_EARTH + 100000.0
    speed_initial = 6.0
    flight_path_angle = np.radians(-80.0)
    angular_momentum = radius_initial * speed_initial * np.cos(flight_path_angle)
    specific_energy = speed_initial**2 / 2.0 - MU_EARTH / radius_initial
    eccentricity = np.sqrt(
        1.0 + 2.0 * specific_energy * angular_momentum**2 / MU_EARTH**2
    )
    semilatus_rectum = angular_momentum**2 / MU_EARTH
    semimajor_axis_magnitude = MU_EARTH / (2.0 * specific_energy)
    true_initial_magnitude = np.arccos(
        (semilatus_rectum / radius_initial - 1.0) / eccentricity
    )
    true_initial = -true_initial_magnitude
    radius_perigee = semilatus_rectum / (1.0 + eccentricity)
    mean_initial = hyperbolic_mean_from_true(true_initial, eccentricity)
    mean_motion = np.sqrt(MU_EARTH / semimajor_axis_magnitude**3)
    if radius_perigee <= R_EARTH:
        true_event = -np.arccos((semilatus_rectum / R_EARTH - 1.0) / eccentricity)
        mean_event = hyperbolic_mean_from_true(true_event, eccentricity)
        outcome = "impact"
    else:
        mean_event = 0.0
        outcome = "flyby"
    time_to_event = (mean_event - mean_initial) / mean_motion
    common = [
        f"e = {eccentricity:.9f}; |a| = {semimajor_axis_magnitude:.6f} km",
        f"perigee radius = {radius_perigee:.6f} km",
        f"perigee altitude = {radius_perigee - R_EARTH:.6f} km",
    ]
    write_output("10a", common + [f"trajectory outcome = {outcome}"])
    write_output(
        "10b",
        [
            f"time to closest approach = {time_to_event:.6f} s "
            f"= {time_to_event / 3600.0:.9f} h",
        ],
    )


def main() -> None:
    problem_02()
    problem_03()
    problem_04()
    problem_05()
    problem_06()
    problem_07()
    problem_08()
    problem_09()
    problem_10()


if __name__ == "__main__":
    main()
