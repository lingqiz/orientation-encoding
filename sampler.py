import numpy as np

def sample_orientation(n_sample, uniform=True):
    # sample from p(theta) = 1/Z * (2 - |sin(theta)|)
    # or from a uniform distribution
    seed = np.random.random(n_sample)
    if uniform:
        return seed * 180

    delta = 0.1
    theta = np.arange(0, 180, delta)

    prob  = 2 - 1.25 * np.abs(np.sin(2 * theta / 180 * np.pi))
    prob  = prob / np.trapz(prob)
    cprob = np.cumsum(prob)

    return np.interp(seed, cprob, theta)
    # find the CDF of the distribution    

# test the sampler
if __name__ == '__main__':
    import matplotlib.pyplot as plt

    # uniform sample
    n_sample = 500
    sample = sample_orientation(n_sample)
    plt.hist(sample, bins=18)
    plt.show()
    
    # sample from natural orientation distribution
    sample = sample_orientation(n_sample, uniform=False)
    plt.hist(sample, bins=18)
    plt.show()
