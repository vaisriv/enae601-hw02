/////////////
// Imports //
/////////////
#import "@preview/adaptable-pset:0.2.0": *
#import "@preview/physica:0.9.8": *
#import "@preview/unify:0.8.1": *
#import "@preview/codly:1.3.0": *
#import "@preview/codly-languages:0.1.1": *
#show: codly-init.with()
#codly(languages: codly-languages)

/////////////////
// Maths Setup //
/////////////////

// upright vectors
#let vectorboldupright(a) = vb($upright(#a)$)
#let vbu = vectorboldupright
#let vectorunitupright(a) = vu($upright(#a)$)
#let vuu = vectorunitupright
#let vectorarrowupright(a) = va($upright(#a)$)
#let vau = vectorarrowupright

// automatically use square brackets for vectors and matricies
#set math.vec(delim: "[")
#set math.mat(delim: "[")
#let vecrowOld = vecrow
#let vecrow = vecrowOld.with(delim: "[")

////////////////////
// Document Setup //
////////////////////

// assignment info
#show: homework.with(
    title: "HW02",
    author: "Vai Srivastava",
    collaborators: [],
    course-id: "ENAE 601: Astrodynamics",
    instructor: "Dr. Healy",
    semester: "Fall 2026",
    due-time: "September 30th. at 23:59",

    // (defaults to A4)
    paper-size: "us-letter",
)

// document settings
#set text(font: "New Computer Modern", size: 10pt)
#set enum(numbering: "a)")

// problem headings
#let probOld = prob
#let prob = prob.with(color: black)

////////////////////////////
// The Assignment Itself: //
// Problems and Solutions //
////////////////////////////

#prob(title: "")[
    Where Curtis says "orbital elements", he substitutes angular momentum for the standard semi-major axis. Show how to compute one from the other.

    #emph[For the following problems and the rest of the semester, compute semi-major axis instead of angular momentum when classical (Keplerian) orbit elements are requested, unless otherwise specified.]
]

We want functions $f(h) = a$ and $g(a) = h$ for specific angular momentum $h = abs(vbu(h))$ and semi-major axis $a$.

Semi-latus rectum $p$ relates to semi-major axis by:
$
    p = a (1 - e^2)
$

and to specific angular momentum by:
$
    p = h^2/mu
$

Equating the two gives:
$
    a (1 - e^2) = h^2/mu
$

Solving for $h$ gives:
$
    h = sqrt(mu a (1 - e^2))
$

and solving for $a$ gives:
$
    a = h^2/(mu (1 - e^2))
$

Thus, we have (as long as $e eq.not 1$):
$
    h & = sqrt(mu a (1 - e^2)) \
    a & = h^2/(mu (1 - e^2)) quad qed
$
<hwk:s01>

#pagebreak(weak: true)

#prob(title: "Curtis 3.5")[
    Calculate the time required to fly from $P$ to $B$, in terms of the eccentricity $e$ and the period $T$. $B$ lies on the minor axis.

    #figure(
        image("../references/p3.5.png", width: 50%),
    ) <fig:p02>
] <hwk:p02>

The time since periapsis for an elliptical orbit, given the mean anomaly and the period is:
$
    M_e = (2 pi)/T t
$

The relation between the mean anomaly and the eccentric anomaly for an elliptical orbit, given the eccentricity, is:
$
    M_e = E - e sin(E)
$

Equating the two gives:
$
    (2 pi)/T t = E - e sin(E)
$

Solving for $t$ gives:
$
    t = (E - e sin(E))/(2 pi) T
$ <eqn:t_E_e_T>

As $B$ is on the minor axis, $E = pi/2$.

Substituting $E = pi/2$ and computing:
$
    t & = (E - e sin(E))/(2 pi) T \
      & = (pi/2 - e sin(pi/2))/(2 pi) T \
      & = (1/4 - e/(2 pi)) T
$

Thus, the time required is:
$
    t = (1/4 - e/(2 pi)) T quad qed
$
<hwk:s02>

#pagebreak(weak: true)

#prob(title: "Curtis 3.6")[
    If the eccentricity of the elliptical orbit is $0.3$, calculate, in terms of the period $T$, the time required to fly from $P$ to $B$.

    #figure(
        image("../references/p3.6.png", width: 50%),
    ) <fig:p03>
] <hwk:p03>

Using #link(<eqn:t_E_e_T>)[our formula for the time since periapsis for an elliptical orbit, given the eccentric anomaly, eccentricity, and the period] from #link(<hwk:s02>)[our solution to Problem 2]:
$
    t = (E - e sin(E))/(2 pi) T
$

The relation between eccentric anomaly and true anomaly is:
$
    E = arccos((e + cos(theta))/(1 + e cos(theta)))
$

Combining these equations, we have:
$
    t = (arccos((e + cos(theta))/(1 + e cos(theta))) - e sin(arccos((e + cos(theta))/(1 + e cos(theta)))))/(2 pi) T
$

As the angle between $B$ and $P$ is #qty(90, "degree"), so $theta = pi/2$.

Substituting $e = 0.3$ and $theta = pi/2$ and computing:
$
    t &= (arccos((e + cos(theta))/(1 + e cos(theta))) - e sin(arccos((e + cos(theta))/(1 + e cos(theta)))))/(2 pi) T \
    &= (arccos((0.3 + cos(pi/2))/(1 + 0.3 cos(pi/2))) - 0.3 sin(arccos((0.3 + cos(pi/2))/(1 + 0.3 cos(pi/2)))))/(2 pi) T \
    &= 0.156 T
$

Thus, the time required is:
$
    t = 0.156 T quad qed
$
<hwk:s03>

#pagebreak(weak: true)

#prob(title: "Curtis 3.8")[
    A satellite is in Earth orbit for which the perigee altitude is #qty(200, "km") and the apogee altitude is #qty(600, "km"). Find the time interval during which the satellite remains above an altitude of #qty(400, "km").
] <hwk:p04>

// TODO:
Answer
<hwk:s04>

#pagebreak(weak: true)

#prob(title: "Curtis 3.9")[
    An Earth-orbiting satellite has a perigee radius of #qty(7000, "km") and an apogee radius of #qty(10000, "km").

    + What true anomaly $Delta theta$ is swept out between $t = qty(0.5, "h")$ and $t = qty(1.5, "h")$ after perigee passage?
    <hwk:p05a>

    + What area is swept out by the position vector during that time interval?
    <hwk:p05b>
] <hwk:p05>

// TODO:
+ Answer
<hwk:s05a>

// TODO:
+ Answer
<hwk:s05b>

#pagebreak(weak: true)

#prob(title: "Curtis 3.10")[
    An Earth-orbiting satellite has a period of #qty(14, "h") and a perigee radius of #qty(10000, "km"). At time $t = qty(10, "h")$ after perigee passage, determine:

    + The radial position.
    <hwk:p06a>

    + The speed.
    <hwk:p06b>

    + The radial component of the velocity.
    <hwk:p06c>
] <hwk:p06>

// TODO:
+ Answer
<hwk:s05a>

// TODO:
+ Answer
<hwk:s05b>

// TODO:
+ Answer
<hwk:s05c>

#pagebreak(weak: true)

#prob(title: "Curtis 3.15")[
    A spacecraft on a parabolic trajectory around the Earth has a perigee radius of #qty(6600, "km").

    + How long does it take to coast from $theta = -qty(90, "degree")$ to $theta = +qty(90, "degree")$?
    <hwk:p06a>

    + How far is the spacecraft from the center of the Earth #qty(36, "h") after passing through perigee?
    <hwk:p06b>
] <hwk:p06>

// TODO:
+ Answer
<hwk:s06a>

// TODO:
+ Answer
<hwk:s06b>

#pagebreak(weak: true)

#prob(title: "Curtis 3.16")[
    A spacecraft on a hyperbolic trajectory around the Earth has a perigee radius of #qty(6600, "km") and a perigee speed of $1.2 v_"esc"$.

    + How long does it take to coast from $theta = -qty(90, "degree")$ to $theta = +qty(90, "degree")$?
    <hwk:p07a>

    + How far is the spacecraft from the center of the Earth #qty(24, "h") after passing through perigee?
    <hwk:p07b>
] <hwk:p07>

// TODO:
+ Answer
<hwk:s07a>

// TODO:
+ Answer
<hwk:s07b>

#pagebreak(weak: true)

#prob(title: "Curtis 3.17")[
    A trajectory has a perigee velocity $1.1 v_"esc"$ and a perigee altitude of #qty(200, "km"). If at 10 a.m., the satellite is travelling towards the Earth with a speed of #qty(8, "km/s"), how far will it be from the Earth's surface at 5 p.m. the same day?
] <hwk:p08>

// TODO:
+ Answer
<hwk:s08>

#pagebreak(weak: true)
#prob(title: "Curtis 3.18")[
    An incoming object is sighted at an altitude of #qty(100000, "km") with a speed of #qty(6, "km/s") and a flight path angle of $-qty(80, "degree")$.

    + Will it impact the Earth or fly by?
    <hwk:p09a>

    + What is the time to impact or to closest approach?
    <hwk:p09b>
] <hwk:p09>

// TODO:
+ Answer
<hwk:s09a>

// TODO:
+ Answer
<hwk:s09b>

#pagebreak(weak: true)
== Code

#codly(header: [./src/index.py])
#raw(read("../src/index.py"), block: true, lang: "python") <code:index.py>
