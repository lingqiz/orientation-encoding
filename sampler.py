import numpy as np
from numpy.random import uniform

def sample_orientation(n_sample, uniform=True):
    # sample from p(theta) = 1/Z * (2 - |sin(theta)|)
    # or from a uniform distribution
    seed = np.random.random(n_sample)
    if uniform:
        return seed * 180

    delta = 0.1
    theta = np.arange(0, 180, delta)

    # probability distribution we would like to sample from
    prob  = 2 - 1.25 * np.abs(np.sin(2 * theta / 180 * np.pi))

    # find the CDF of the distribution
    prob  = prob / np.trapz(prob)
    cprob = np.cumsum(prob)

    return np.interp(seed, cprob, theta)    

def sample_stimuli(n_sample, mode='uniform'):
    # using stratified sampling over [0, 1] to ensure uniformity
    edges = np.linspace(0, 1, n_sample + 1)
    samples = np.array([uniform(edges[idx], edges[idx+1]) for idx in range(n_sample)])

    if mode == 'uniform':
        np.random.shuffle(samples)
        return samples * 180

    delta = 0.1
    theta = np.arange(0, 180, delta)
    if mode == 'cardinal':
        prob = 2 - 1.25 * np.abs(np.sin(2 * theta / 180 * np.pi))
    elif mode == 'oblique':
        prob = 2 - 1.25 * np.abs(np.cos(2 * theta / 180 * np.pi))
    else:
        raise ValueError('sample mode is invalid')
        
    prob  = prob / np.trapz(prob)
    cprob = np.cumsum(prob)
    
    np.random.shuffle(samples)
    return np.interp(samples, cprob, theta)
        
# test the sampler
if __name__ == '__main__':
    import matplotlib.pyplot as plt
    
    # uniform sample
    n_sample = 200
    # sample = sample_orientation(n_sample)
    sample = sample_stimuli(n_sample, mode='uniform')
    plt.hist(sample, bins=20)
    plt.show()
    
    # sample from natural orientation distribution
    # sample = sample_orientation(n_sample, uniform=False)
    sample = sample_stimuli(n_sample, mode='cardinal')
    plt.hist(sample, bins=20)
    plt.show()

    sample = sample_stimuli(n_sample, mode='oblique')
    plt.hist(sample, bins=20)
    plt.show()

