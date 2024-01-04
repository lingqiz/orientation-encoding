import numpy as np
import scipy.io as sio
from analysis.ornt import slide_average
from scipy.interpolate import splev, splrep

def behavior_analysis(cond, data_smooth=2.5, fi_smooth=5e-3):
    # load behavioral data
    mat_data = sio.loadmat('./data/%s.mat' % cond)

    # extract data variables
    support = mat_data['support']
    average = mat_data['average']
    stdv = mat_data['stdv']
    fisher = mat_data['fisher']

    # bootstrap runs
    allAverage = mat_data['allAverage']
    allStdv = mat_data['allStdv']
    allFisher = mat_data['allFisher']

    # reshape fisher information
    indice = (support > 1.0) & (support < 179.0)
    fi_axis = support[indice].squeeze()
    fisher = fisher[indice].squeeze()
    allFisher = allFisher[indice.squeeze(), :]

    fi_axis[fi_axis > 90] -= 180
    resort = np.argsort(fi_axis)
    fi_axis = fi_axis[resort]
    fisher = fisher[resort]
    allFisher = allFisher[resort, :]

    # change axis to [-90, 90]
    support[support > 90] -= 180
    support = np.squeeze(support)
    resort = np.argsort(support)
    support = support[resort]

    data = [average, stdv]
    bootstrap = [allAverage, allStdv]
    for i in range(len(data)):
        data[i] = np.squeeze(data[i])
        data[i] = data[i][resort]
        bootstrap[i] = bootstrap[i][resort, :]

    # smooth the data with spline fit
    for i in range(len(data)):
        spl = splrep(support, data[i], s=data_smooth)
        data[i] = splev(support, spl)

        for j in range(bootstrap[i].shape[1]):
            spl = splrep(support, bootstrap[i][:, j], s=data_smooth)
            bootstrap[i][:, j] = splev(support, spl)

    # resample fisher information to the same axis
    # with spline smoothing
    spl = splrep(fi_axis, fisher, s=fi_smooth)
    fisher = splev(support, spl)
    data.append(fisher)

    resampleFisher = np.zeros((len(support), allFisher.shape[1]))
    for i in range(allFisher.shape[1]):
        spl = splrep(fi_axis, allFisher[:, i], s=fi_smooth)
        resampleFisher[:, i] = splev(support, spl)
    bootstrap.append(resampleFisher)

    return support, data, bootstrap

def fisher_base(ornt, snd):
    '''
    Compute the normalized Fisher information for the baseline condition
    '''
    # flip orientation
    ornt[ornt < 0] *= -1

    # config the sliding average
    center = [-5, 10, 20, 35, 50, 65, 80, 95]
    window = 15
    config = {'center' : center,
            'lb' : 0, 'ub' : 90, 'cyclical' : False}

    # sliding average
    axis, fi_avg = slide_average(ornt, snd, np.mean, window, config)
    error = slide_average(ornt, snd, np.std, window, config)[-1]
    n_data = slide_average(ornt, snd, np.size, window, config)[-1]
    error = error / np.sqrt(n_data)

    # compute normalized fisher information
    fisher = np.sqrt(-fi_avg)
    fi_error = error / (2 * fisher)

    convert = 180 / (2 * np.pi)
    scale = 1 / np.trapz(fisher, axis / convert) / 2
    fisher *= scale
    fi_error *= scale

    return axis, fisher, fi_error