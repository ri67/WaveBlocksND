"""The WaveBlocks Project

Asymptotic approximation to Hermite polynomials of very high degree.

@author: R. Bourquin
@copyright: Copyright (C) 2015, 2016 R. Bourquin
@license: Modified BSD License
"""

from numpy import (sqrt, log, sin, cos, arccos, sinh, cosh, arccosh, exp,
                   zeros_like, floating, atleast_1d)
from scipy.special import airy


def pbcf_series(mu, ct, zeta, phi):
    r"""Asymptotic series expansion of parabolic cylinder function:

    .. math:: U\left(-\frac{1}{2}\mu^{2},\mu t\sqrt{2}\right)

    :param mu: The value of :math:`\mu = 2n + 1`
    :param ct: The value of :math:`t = \frac{x}{\sqrt{\mu}}`
    :param zeta: The value of :math:`\zeta`
    :param phi: The value of :math:`\phi(\zeta)`
    """
    # Coefficients
    # http://dlmf.nist.gov/12.10#E43
    a0 =  1.0
    a1 =  0.10416666666666666667
    a2 =  0.08355034722222222222
    a3 =  0.12822657455632716049
    a4 =  0.29184902646414046425
    a5 =  0.88162726744375765242
    b0 =  1.0
    b1 = -0.14583333333333333333
    b2 = -0.09874131944444444444
    b3 = -0.14331205391589506173
    b4 = -0.31722720267841354810
    b5 = -0.94242914795712024914
    a = (a0, a1, a2, a3, a4, a5)
    b = (b0, b1, b2, b3, b4, b5)
    # Polynomials
    # http://dlmf.nist.gov/12.10#E9
    u0 = 1.0
    u1 = (       1.0*ct**3  -         6.0*ct) / 24.0
    u2 = (      -9.0*ct**4  +       249.0*ct**2  +        145.0) / 1152.0
    u3 = (   -4042.0*ct**9  +     18189.0*ct**7  -      28287.0*ct**5  -     151995.0*ct**3 -     259290.0*ct) / 414720.0
    u4 = (   72756.0*ct**10 -    321339.0*ct**8  -     154982.0*ct**6  +   50938215.0*ct**4 +  122602962.0*ct**2 +    12773113.0) / 39813120.0
    u5 = (82393456.0*ct**15 - 617950920.0*ct**13 + 1994971575.0*ct**11 - 3630137104.0*ct**9 + 4433574213.0*ct**7 - 37370295816.0*ct**5 - 119582875013.0*ct**3 - 34009066266.0*ct) / 6688604160.0
    u = (u0, u1, u2, u3, u4, u5)
    # Airy Evaluation (Bi and Bip unused)
    Ai, Aip, Bi, Bip = airy(mu**(4.0/6.0) * zeta)
    # Terms for U
    # http://dlmf.nist.gov/12.10#E42
    A0 =   b[0]*u[0]
    A1 =  (b[2]*u[0] + phi**6*b[1]*u[1] + phi**12*b[0]*u[2]) / zeta**3
    A2 =  (b[4]*u[0] + phi**6*b[3]*u[1] + phi**12*b[2]*u[2] + phi**18*b[1]*u[3] + phi**24*b[0]*u[4]) / zeta**6
    B0 = -(a[1]*u[0] + phi**6*a[0]*u[1]) / zeta**2
    B1 = -(a[3]*u[0] + phi**6*a[2]*u[1] + phi**12*a[1]*u[2] + phi**18*a[0]*u[3]) / zeta**5
    B2 = -(a[5]*u[0] + phi**6*a[4]*u[1] + phi**12*a[3]*u[2] + phi**18*a[2]*u[3] + phi**24*a[1]*u[4] + phi**30*a[0]*u[5]) / zeta**8
    # U
    # http://dlmf.nist.gov/12.10#E35
    U = phi * (Ai  * (A0 + A1/mu**2.0 + A2/mu**4.0) +
               Aip * (B0 + B1/mu**2.0 + B2/mu**4.0) / mu**(8.0/6.0))
    return U


def pbcf_asy_s(n, t):
    r"""Asymptotic series expansion of parabolic cylinder function:

    .. math:: U\left(-\frac{1}{2}\mu^{2},\mu t\sqrt{2}\right)

    for :math:`0 \leq t < 1`.

    :param n: The order :math:`n`
    :param t: The rescaled variable :math:`t`
    """
    theta = arccos(t)
    st = sin(theta)
    ct = cos(theta)
    # http://dlmf.nist.gov/12.10#vii
    mu = 2.0 * n + 1.0
    # http://dlmf.nist.gov/12.10#E23
    eta = 0.5 * theta - 0.5 * st * ct
    # http://dlmf.nist.gov/12.10#E39
    zeta = -(3.0 * eta / 2.0) ** (2.0 / 3.0)
    # http://dlmf.nist.gov/12.10#E40
    phi = (-zeta / st**2) ** (0.25)
    return pbcf_series(mu, ct, zeta, phi)


def pbcf_asy_l(n, t):
    r"""Asymptotic series expansion of parabolic cylinder function:

    .. math:: U\left(-\frac{1}{2}\mu^{2},\mu t\sqrt{2}\right)

    for :math:`1 < t`.

    :param n: The order :math:`n`
    :param t: The rescaled variable :math:`t`
    """
    theta = arccosh(t)
    st = sinh(theta)
    ct = cosh(theta)
    # http://dlmf.nist.gov/12.10#vii
    mu = 2.0 * n + 1.0
    # http://dlmf.nist.gov/12.10#E23
    eta = 0.5 * st * ct - 0.5 * log(st + ct)
    # http://dlmf.nist.gov/12.10#E39
    zeta = (3.0 * eta / 2.0) ** (2.0 / 3.0)
    # http://dlmf.nist.gov/12.10#E40
    phi = (zeta / st**2) ** (0.25)
    return pbcf_series(mu, ct, zeta, phi)


def pbcf_asy_tp(n, t):
    r"""Asymptotic series expansion of parabolic cylinder function:

    .. math:: U\left(-\frac{1}{2}\mu^{2},\mu t\sqrt{2}\right)

    for :math:`t \approx 1`. This is the turning point special case.

    :param n: The order :math:`n`
    :param t: The rescaled variable :math:`t`
    """
    mu = 2.0 * n + 1.0
    # Series inversion
    zeta = (-1.1154602376350014386 + 0.94683206534259310319*t + 0.20092390951413596864*t**2 - 0.044104995690190539136*t**3 +
            0.017469790174220817687*t**4 - 0.0088287554164487068288*t**5 + 0.0051211352582927995985*t**6 - 0.0032244338764873460755*t**7 +
            0.0021125921956647975404*t**8 - 0.0013843459602562093761*t**9 + 0.00087302390087403782068*t**10 - 0.00051134856243343516386*t**11 +
            0.00026957449214014972347*t**12 - 0.00012440612318221805202*t**13 + 0.000048963028297618756177*t**14 - 0.000015993129143629483122*t**15 +
            4.1983046448762575472*10**-6*t**16 - 8.4840463365499518479*10**-7*t**17 + 1.2360723726177868995*10**-7*t**18 - 1.1537952829608371539*10**-8*t**19 +
            5.1762857628454208175*10**-10*t**20)
    phi = (1.0276932750036503140 - 0.21808283408806466225*t + 0.14122174457564771016*t**2 - 0.10816400897094073140*t**3 +
           0.088874166058550695301*t**4 - 0.075714541592906584263*t**5 + 0.065443222791321861057*t**6 - 0.056156780196999485459*t**7 +
           0.046662565448600134022*t**8 - 0.036547770139551846069*t**9 + 0.026279904347178909432*t**10 - 0.016935586586706330798*t**11 +
           0.0095718282783427771267*t**12 - 0.0046495457010873127526*t**13 + 0.0019014010421815025206*t**14 - 0.00063945223108083177494*t**15 +
           0.00017170521340783134157*t**16 - 0.000035325775105885003427*t**17 + 5.2214994798105409241*10**-6*t**18 - 4.9317900171943814621*10**-7*t**19 +
           2.2343423148466235499*10**-8*t**20)
    # Airy Evaluation (Bi and Bip unused)
    Ai, Aip, _, _ = airy(mu**(4.0 / 6.0) * zeta)
    # Terms for U
    # http://dlmf.nist.gov/12.10#E42
    A0 = 1.0
    A1 = -0.0086458333333333333333 + 0.0088247644520537323073*zeta - 0.0074183103614150198401*zeta**2 + 0.0053175928144826954351*zeta**3 - 0.0036749699295810273907*zeta**4 + 0.0024548403578794918840*zeta**5
    A2 =  0.0061297344505962282500 - 0.0094387404479761494580*zeta + 0.011065789808355794898*zeta**2  - 0.011160126023304710852*zeta**3  + 0.010218849174417654722*zeta**4  - 0.0087256605902535063232*zeta**5
    B0 = -0.040497462318049494582  + 0.015555555555555555556*zeta  - 0.0080047422249528129358*zeta**2 + 0.0041844376699171406787*zeta**3 - 0.0023557992011138269642*zeta**4 + 0.0013016588855262778612*zeta**5
    B1 =  0.014067425869597622078  - 0.010583886849378850867*zeta  + 0.0088855396810720634546*zeta**2 - 0.0071105198593437325742*zeta**3 + 0.0054283720667346030128*zeta**4 - 0.0039819488927847170035*zeta**5
    B2 = -0.021934053543058220142  + 0.022346550505843322786*zeta  - 0.024595927387236822024*zeta**2  + 0.025053467465276891847*zeta**3  - 0.023734309391991717696*zeta**4  + 0.021194552738417480440*zeta**5
    # U
    # http://dlmf.nist.gov/12.10#E35
    U = phi * (Ai  * (A0 + A1 / mu**2.0 + A2 / mu**4.0) +
               Aip * (B0 + B1 / mu**2.0 + B2 / mu**4.0) / mu**(8.0 / 6.0))
    return U


def hermite_asy_pos(n, x):
    r"""Expand the Hermite function :math:`h_n(x)` in terms
    of the parabolic cylinder function :math:`U`. The scalar
    prefactor is omitted. This function uses asymptotic formulas
    and is accurate to machine precision for about :math:`n > 100`.
    The variable :math:`x` must have a non-negative real value.

    :param n: The order :math:`n`
    :param x: The variable :math:`x`
    """
    # Rescale the x values
    mu = sqrt(2.0 * n + 1.0)
    t = x / mu
    # Bound the region around the turning point
    tau = (2.220446049250313e-16)**(0.125) / mu
    lower = 1.0 - 2 * 0.5 * (3 * tau)**(2.0 / 3.0)
    upper = 1.0 + 2 * 0.5 * (3 * tau)**(2.0 / 3.0)
    # Indices for all regions
    ilo = t < lower
    iup = t > upper
    ipa = ~(ilo | iup)
    # Evaluate for each region separately
    y = zeros_like(t)
    y[ilo] = pbcf_asy_s(n, t[ilo])
    y[ipa] = pbcf_asy_tp(n, t[ipa])
    y[iup] = pbcf_asy_l(n, t[iup])
    return y


def get_tau(n):
    r"""Compute the scalar prefactor :math:`\tau(n)`.

    :param n: The order :math:`n`
    """
    d = (n + 1) + 1 / (12 * (n + 1) - 1 / (10 * (n + 1)))
    tauexp = 1 / 4 - (n / 2 - 1 / 4) * log(2) - ((n + 1) / 2) * log(d) + (n + 1 / 3) * log(sqrt(2 * n + 1)) + log(n + 1) / 4
    gams = [1.0, -1 / 24.0, 1 / 1152.0, 1003 / 414720.0, -4027 / 39813120.0]
    s = 1.0 + 0.5 * (sum(gams[i] / (n + 0.5)**i for i in range(1, 5)))
    tau = s * exp(tauexp)
    return tau


def hermite_asy(n, x):
    r"""Expand the Hermite function :math:`h_n(x)` in terms
    of the parabolic cylinder function :math:`U`. This function
    uses asymptotic formulas and is accurate to machine precision
    for about :math:`n > 100`. The variable :math:`x` can be any
    small or large value on the real axis.

    :param n: The order :math:`n`
    :param x: The variable :math:`x`
    """
    x = atleast_1d(x)
    neg = x < 0
    pos = x > 0
    y = zeros_like(x, dtype=floating)
    y[neg] = (-1)**(n % 2) * hermite_asy_pos(n, -x[neg])
    y[pos] = hermite_asy_pos(n, x[pos])
    tau = get_tau(n)
    return tau * y
