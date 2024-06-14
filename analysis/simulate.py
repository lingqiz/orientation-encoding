import pyrtools as pt
import numpy as np

class VoxelSimuate():

    def __init__(self, lyr_idx, order=15, height='auto', weight=None):
        self.lyr_idx = lyr_idx
        self.order = order
        self.height = height

        if weight is None:
            self.weight = 1 / (order + 1) * np.ones(order + 1)
        else:
            self.weight = weight

    def voxel_response(self, image):
        pyr = pt.pyramids.SteerablePyramidFreq(image, order=self.order,
                                               height=self.height,
                                               is_complex=True)

        s = self.lyr_idx
        all_resp = np.zeros((pyr.num_orientations, *pyr.pyr_coeffs[(s, 0)].shape))
        for c in range(pyr.num_orientations):
            band_re = pyr.pyr_coeffs[(s, c)].real
            band_im = pyr.pyr_coeffs[(s, c)].imag

            # sum of square responses
            all_resp[c] = np.sqrt(band_re**2 + band_im**2) * self.weight[c]

        return np.sum(all_resp, axis=0)