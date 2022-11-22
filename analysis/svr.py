import numpy as np
from sklearn.svm import SVR

class RegressDecode():
    def __init__(self) -> None:
        self.range = 180.0
        self.svr = []

    def fit_model(self, stim, resp, epsilon=0.0, lda=1.0):
        stim = stim / self.range * 2 * np.pi
        sin = np.sin(stim)
        cos = np.cos(stim)

        for target in [sin, cos]:
            svr_obj = SVR(kernel='linear', epsilon=epsilon, C=lda)
            svr_obj.fit(resp.T, target)
            self.svr.append(svr_obj)

    def decode(self, resp):
        sin, cos = [decoder.predict(resp.T) for
                    decoder in self.svr]
        est = np.arctan2(sin, cos)
        est[est < 0] += (2 * np.pi)

        return est / (2 * np.pi) * self.range