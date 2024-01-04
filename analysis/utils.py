import numpy as np
import scipy.io as sio
from analysis.ornt import slide_average
from scipy.interpolate import splev, splrep
from scipy import stats

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

def neural_analysis(roi):
    N_SUB = 10
    N_COND = 3
    COUNT = 1600

    data_path = './data/roi/ORNT_Fisher_{}.npy'.format(roi)

    with open(data_path, 'rb') as fl:
        all_ornt = np.load(fl)
        _ = np.load(fl)
        all_snd = np.load(fl)

    # change axis
    cmb_ornt = np.transpose(all_ornt, (1, 0, 2)).reshape(N_COND, N_SUB * COUNT)
    cmb_snd = np.transpose(all_snd, (1, 0, 2)).reshape(N_COND, N_SUB * COUNT)
    cmb_ornt[cmb_ornt > 90] -= 180

    return cmb_ornt, cmb_snd

def _combine_surr(ornt, snd):
    '''
    Combine data from the two surround conditions
    '''
    # context 1
    ornt_cxt1, snd_cxt1 = (ornt[0], snd[0])

    # context 2 + mirroring
    ornt_cxt2, snd_cxt2 = (ornt[1], snd[1])
    ornt_cxt2 *= -1

    # combine
    ornt_adpt = np.concatenate([ornt_cxt1, ornt_cxt2])
    snd_adpt = np.concatenate([snd_cxt1, snd_cxt2])

    return ornt_adpt, snd_adpt

def normalize_fisher(axis, fi_avg, error, fold=1):
    '''
    Normalize the fisher information
    '''
    # compute normalized fisher information
    fisher = np.sqrt(-fi_avg)
    fi_error = error / (2 * fisher)

    convert = 180 / (2 * np.pi)
    scale = 1 / np.trapz(fisher, axis / convert) / fold
    fisher *= scale
    fi_error *= scale

    return axis, fisher, fi_error

def fisher_base(ornt, snd, normalize=True):
    '''
    Compute the normalized Fisher information for the baseline condition
    '''
    # flip orientation
    ornt[ornt < 0] *= -1

    # config the sliding average
    center = [-5, 10, 20, 35, 50, 65, 80, 95]
    window = 12.5
    config = {'center' : center, 'lb' : 0, 'ub' : 90, 'cyclical' : False}

    # sliding average
    axis, fi_avg = slide_average(ornt, snd, np.mean, window, config)
    error = slide_average(ornt, snd, np.std, window, config)[-1]
    n_data = slide_average(ornt, snd, np.size, window, config)[-1]
    error = error / np.sqrt(n_data)

    if not normalize:
        return axis, -fi_avg, error

    return normalize_fisher(axis, fi_avg, error, fold=2)

def fisher_surround(ornt, snd, normalize=True):
    '''
    Compute the normalized Fisher information for the surround condition
    '''
    # combine the two contexts conditions
    ornt_adpt, snd_adpt = _combine_surr(ornt, snd)

    # config the sliding average
    center = np.array([10, 20, 35, 50, 65, 80, 95])
    center = np.concatenate([-center[::-1], [0], center])
    window = 12.5
    config = {'center' : center, 'lb' : -90, 'ub' : 90, 'cyclical' : False}

    # sliding average
    axis, fi_avg = slide_average(ornt_adpt, snd_adpt, np.mean, window, config)
    error = slide_average(ornt_adpt, snd_adpt, np.std, window, config)[-1]
    n_data = slide_average(ornt_adpt, snd_adpt, np.size, window, config)[-1]
    error = error / np.sqrt(n_data)

    if normalize:
        axis, fisher, error = normalize_fisher(axis, fi_avg, error, fold=1)
    else:
        fisher = -fi_avg

    # split the data into with and without surround
    zero_idx = int(np.where((axis == 0))[0][0])
    with_surr = [axis[zero_idx:], fisher[zero_idx:], error[zero_idx:]]
    no_surr = [-axis[:zero_idx+1][::-1],
               fisher[:zero_idx+1][::-1],
               error[:zero_idx+1][::-1]]

    return with_surr, no_surr

def modulation_index(roi):
    '''
    Compute the modulation index
    '''
    # load data
    ornt, snd = neural_analysis(roi)
    ornt, snd = _combine_surr(ornt[1:], snd[1:])

    with_surr = snd[(ornt > 22.5) & (ornt < 47.5)]
    no_surr = snd[(ornt > -47.5) & (ornt < -22.5)]

    # compute modulation index
    base = np.abs(np.mean(no_surr))
    delta = np.abs(np.mean(with_surr)) - base

    svm = np.var(with_surr) / len(with_surr) \
        + np.var(no_surr) / len(no_surr)
    sem = np.sqrt(svm)

    # compute p-value
    p_val = stats.ttest_ind(with_surr, no_surr)[1]
    return np.mean(-snd), delta, sem, p_val
