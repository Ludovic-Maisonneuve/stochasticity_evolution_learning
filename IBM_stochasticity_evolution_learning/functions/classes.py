import numpy as np
import sdeint


class Environment:
    def __init__(self, f_0, s_0, beta_v, beta_o, alpha, eps, rho, sigma_vl, sigma_ol, sigma_i, eta_f, eta_s, theta,
                 gamma, P_mut, mutation_step):
        # Initialize environment parameters
        self.f_0, self.s_0, self.beta_v, self.beta_o, self.alpha, self.eps, self.rho, self.sigma_vl, self.sigma_ol, self.sigma_il, self.eta_f, self.eta_s, self.theta, self.gamma, self.P_mut, self.mutation_step = f_0, s_0, beta_v, beta_o, alpha, eps, rho, sigma_vl, sigma_ol, sigma_i, eta_f, eta_s, theta, gamma, P_mut, mutation_step


def get_knowledge(v, o, l, k_v, k_o, E):
    # Get parameters' values
    f_0, s_0, beta_v, beta_o, alpha, eps, rho, sigma_vl, sigma_ol, sigma_il, eta_f, eta_s, theta, gamma = E.f_0, E.s_0, E.beta_v, E.beta_o, E.alpha, E.eps, E.rho, E.sigma_vl, E.sigma_ol, E.sigma_il, E.eta_f, E.eta_s, E.theta, E.gamma

    # Compute vertical and oblique cultural heritability
    h_v = (1 - eps) * (1 - np.exp(-l * beta_v * v)) * (1 - rho + rho * np.exp(-l * beta_o * o))
    h_o = (1 - eps) * (1 - np.exp(-l * beta_o * o))

    # Compute the knowledge of the focal individual
    if sigma_vl == 0 and sigma_ol == 0:
        k = h_v * k_v + h_o * k_o + (1 - v - o) * l * alpha + np.random.normal(0, l * sigma_il * np.sqrt(1 - v - o))
        return max(k, 0)

    else:
        # vertical learning
        if v > 0 and sigma_vl > 0:
            tspan = np.linspace(0.0, v, 101)
            k_0 = 0

            def f(x, t):
                return l * beta_v * ((1 - eps) * k_v - x)

            def g(x, t):
                return l * sigma_vl * ((1 - eps) * k_v - x)

            k_v_end = sdeint.itoint(f, g, k_0, tspan)[-1][0]
        else:
            k_v_end = (1 - eps) * (1 - np.exp(-l * beta_v * v)) * k_v

            # oblique learning
        if o > 0 and sigma_ol > 0:
            tspan = np.linspace(0.0, o, 101)

            def f(x, t):
                return l * beta_o * ((1 - eps) * k_o - rho * k_v_end - (x - k_v_end))

            def g(x, t):
                return l * sigma_ol * ((1 - eps) * k_o - rho * k_v_end - (x - k_v_end))

            k_o_end = sdeint.itoint(f, g, k_v_end, tspan)[-1][0]
        else:
            k_o_end = k_v_end + (1 - eps) * (1 - np.exp(-l * beta_o * o)) * (k_o - rho * k_v_end)
        # individual learning
        k = k_o_end + (1 - v - o) * l * alpha + np.random.normal(0, l * sigma_il * np.sqrt((1 - v - o)))
        return max(k, 0)


class Individual:
    def __init__(self, v, o, l, k_v, k_o, N, E, k=None):
        # Initialize individual parameters
        self.v, self.o, self.l, self.k_v, self.k_o, self.N, self.E = v, o, l, k_v, k_o, N, E
        if k is None:
            self.k = get_knowledge(v, o, l, k_v, k_o, E)
        else:
            self.k = k

    def get_fecundity(self):
        # Get parameters' values
        E = self.E
        f_0, s_0, beta_v, beta_o, alpha, eps, rho, sigma_vl, sigma_ol, sigma_il, eta_f, eta_s, theta, gamma = E.f_0, E.s_0, E.beta_v, E.beta_o, E.alpha, E.eps, E.rho, E.sigma_vl, E.sigma_ol, E.sigma_il, E.eta_f, E.eta_s, E.theta, E.gamma
        f = (f_0 + eta_f * self.k) * (1 - self.l) ** theta
        return f

    def get_survival(self, N_o):
        # Get parameters' values
        E = self.E
        f_0, s_0, beta_v, beta_o, alpha, eps, rho, sigma_vl, sigma_ol, sigma_il, eta_f, eta_s, theta, gamma = E.f_0, E.s_0, E.beta_v, E.beta_o, E.alpha, E.eps, E.rho, E.sigma_vl, E.sigma_ol, E.sigma_il, E.eta_f, E.eta_s, E.theta, E.gamma
        s = (s_0 + eta_s * self.k) / (
                1 + gamma * N_o)

        if s > 1:
            print('Error: s>1')
        return max(s, 0)


def initial_generation(v_0, o_0, l_0, k_v0, k_o0, N_0, E):
    # Generate a list of individuals with the specified parameters
    G = [Individual(v_0, o_0, l_0, k_v0, k_o0, N_0, E) for i in range(N_0)]
    return G
