import pyrtools as pt
import numpy as np
from PIL import Image
import cv2

class VoxelSimuate():
    '''
    Simulate voxel response to images
    based on steerable pyramid
    '''

    def __init__(self, pyr_idx, order=15, height='auto', weight=None, complex=True):
        self.pyr_idx = pyr_idx
        self.order = order
        self.height = height
        self.pyr = None

        if weight is None:
            self.weight = 1 / (order + 1) * np.ones(order + 1)
        else:
            self.weight = weight

        self.complex = complex

    def build_pyramid(self, image):
        pyr = pt.pyramids.SteerablePyramidFreq(image, order=self.order,
                                               height=self.height,
                                               is_complex=self.complex)
        self.pyr = pyr

    def voxel_response(self, image):
        if self.pyr is None:
            self.build_pyramid(image)

        s = self.pyr_idx
        all_resp = np.zeros((self.pyr.num_orientations, *self.pyr.pyr_coeffs[(s, 0)].shape))
        for c in range(self.pyr.num_orientations):
            if self.complex:
                band_re = self.pyr.pyr_coeffs[(s, c)].real
                band_im = self.pyr.pyr_coeffs[(s, c)].imag

                # sum of square responses
                all_resp[c] = np.sqrt(band_re**2 + band_im**2) * self.weight[c]

            else:
                all_resp[c] = np.abs(self.pyr.pyr_coeffs[(s, c)]) * self.weight[c]

        return np.sum(all_resp, axis=0)


def voxel_response(image, height='auto'):
    '''
    Average response across orientations
    channels to simulate an "un-tuned" voxel
    '''
    pyr = pt.pyramids.SteerablePyramidFreq(image, height=height,
                                           order=5, is_complex=True)

    # sum orientation responses within each scale
    response_map = []
    for s in range(pyr.num_scales):

        all_resp = np.zeros((pyr.num_orientations, *pyr.pyr_coeffs[(s, 0)].shape))
        for c in range(pyr.num_orientations):
            band_re = pyr.pyr_coeffs[(s, c)].real
            band_im = pyr.pyr_coeffs[(s, c)].imag

            # sum of square responses
            all_resp[c] = np.sqrt(band_re**2 + band_im**2)

        # average response
        avg_resp = np.mean(all_resp, axis=0)
        response_map.append(avg_resp)

    return response_map

def all_response(base_path):
    '''
    './docs/Stimulus/unornt/' OR
    './docs/Stimulus/surr_fixed/'
    '''
    ornt = np.arange(0, 180, 1)
    ornt_resp = []

    for o in ornt:
        stim = Image.open(base_path + f'stim_{o}.png')
        stim = np.array(stim).astype(float)
        ornt_resp.append(voxel_response(stim))

    return ornt_resp

def norm_fi(ornt_resp):
    # Compute FI
    fi_val = []
    for idx in range(len(ornt_resp) - 1):
        delta = ornt_resp[idx + 1] - ornt_resp[idx]
        fi = np.linalg.norm(delta.flatten())
        fi_val.append(np.sqrt(fi))
    fi_val = np.array(fi_val)

    # Normalize FI
    ornt = np.arange(-90, 90, 1)
    fi_wrap = np.concatenate([fi_val[-89:], fi_val[:90]])
    norm_fi = fi_wrap / (np.trapz(fi_wrap, ornt[:-1]) / 180 * 2 * np.pi)

    return ornt[:-1], norm_fi


PATH_BASE = './docs/Stimulus/unornt/'
PATH_SURR = './docs/Stimulus/surr_fixed/'

class PyramidSimulate():
    def __init__(self, cond):
        if cond == 'base':
            self.ornt_resp = all_response(PATH_BASE)

        elif cond == 'surr':
            self.ornt_resp = all_response(PATH_SURR)

    def set_level(self, level, index=None):
        level_resp = []
        for r in self.ornt_resp:
            if index is None:
                index = np.ones_like(r[level]).astype(bool)

            level_resp.append(r[level][index])

        self.level_resp = level_resp

    def combine_level(self, levels=[2, 3, 4]):
        combined_resp = []

        for r in self.ornt_resp:
            combined = np.zeros_like(r[levels[-1]])
            for l in levels:
                combined += cv2.resize(r[l], combined.shape)

            combined_resp.append(combined)

        self.combined_resp = combined_resp

    def select_roi(self, lb, ub, level):
        # total stimulus radius 15.5 deg
        # center: 1.5 - 7 degree; surround 7 - 12.5 degree

        length = self.ornt_resp[0][level].shape[0]
        radius = length / 2

        total = 15.5
        lb = lb / total * radius
        ub = ub / total * radius

        # select pixel within ROI based on radius to the center
        center = length / 2
        x = np.arange(0, length)
        y = np.arange(0, length)
        x, y = np.meshgrid(x, y)
        z = np.zeros_like(x)
        for i in range(length):
            for j in range(length):
                z[i, j] = np.sqrt((x[i, j] - center)**2 + (y[i, j] - center)**2)

        index = np.logical_and(z >= lb, z <= ub)
        self.set_level(level, index=index)

        return index
