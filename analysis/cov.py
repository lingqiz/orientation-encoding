import numpy as np
from numpy import linalg as lin
from sklearn.covariance import LedoitWolf
from dataclasses import dataclass

@dataclass
class SampleCovariance:
    mu: np.array
    cov: np.array
    pri: np.array

def lw_estimate(sample):
    '''
    sample: (n_feature, n_samples)
    '''
    lw = LedoitWolf().fit(sample.T)
    return SampleCovariance(lw.location_.reshape(((-1, 1))),
                            lw.covariance_, lw.precision_)

def kl_div(p, q):
    '''
    KL divergence between two multivariable Gaussian distribution
    '''
    log_det = lin.slogdet(q.cov)[-1] - lin.slogdet(p.cov)[-1]
    k = p.cov.shape[0]
    quad = (p.mu - q.mu).T @ lin.solve(q.cov, p.mu - q.mu)
    tr = np.trace(lin.solve(q.cov, p.cov))

    return 0.5 * (log_det - k + quad + tr)
