import pyrtools as pt
import numpy as np

class VoxelSimuate():
    '''
    Simulate voxel response to images
    based on steerable pyramid
    '''

    def __init__(self, pyr_idx, order=15, height='auto', weight=None, complex=True):
        self.pyr_idx = pyr_idx
        self.order = order
        self.height = height

        if weight is None:
            self.weight = 1 / (order + 1) * np.ones(order + 1)
        else:
            self.weight = weight

        self.complex = complex

    def voxel_response(self, image):
        pyr = pt.pyramids.SteerablePyramidFreq(image, order=self.order,
                                               height=self.height,
                                               is_complex=self.complex)

        s = self.pyr_idx
        all_resp = np.zeros((pyr.num_orientations, *pyr.pyr_coeffs[(s, 0)].shape))
        for c in range(pyr.num_orientations):
            if self.complex:
                band_re = pyr.pyr_coeffs[(s, c)].real
                band_im = pyr.pyr_coeffs[(s, c)].imag

                # sum of square responses
                all_resp[c] = np.sqrt(band_re**2 + band_im**2) * self.weight[c]

            else:
                all_resp[c] = np.abs(pyr.pyr_coeffs[(s, c)]) * self.weight[c]

        return np.sum(all_resp, axis=0)