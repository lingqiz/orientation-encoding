import numpy as np
from numpy import linalg as lin
from sklearn.covariance import LedoitWolf, OAS
from dataclasses import dataclass

@dataclass
class SampleCovariance:
    mu: np.array
    cov: np.array
    pri: np.array

def cov_object(estimator):
    return SampleCovariance(estimator.location_.reshape(((-1, 1))),
                            estimator.covariance_,
                            estimator.precision_)

def lw_estimate(sample):
    '''
    sample: (n_feature, n_samples)
    '''
    lw = LedoitWolf().fit(sample.T)
    return cov_object(lw)

def oas_estimate(sample):
    '''
    sample: (n_feature, n_samples)
    '''
    oas = OAS().fit(sample.T)
    return cov_object(oas)

def kl_div(p, q):
    '''
    KL divergence between two multivariate Gaussian distribution
    '''
    log_det = lin.slogdet(q.cov)[-1] - lin.slogdet(p.cov)[-1]
    k = p.cov.shape[0]
    quad = (p.mu - q.mu).T @ lin.solve(q.cov, p.mu - q.mu)
    tr = np.trace(lin.solve(q.cov, p.cov))

    return 0.5 * (log_det - k + quad + tr).squeeze()
