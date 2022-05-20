import torch, math, einops, numpy as np
from torch.autograd.functional import jacobian

class VoxelEncode():

    @staticmethod
    def tuning(stim, pref):
        '''
        Orientation (basis) tuning function
        '''
        stim = einops.repeat(stim, 'n -> n k', k = pref.shape[0])
        nonlinr = torch.cos(math.pi * (stim - pref) / 90.0)
        rectify = torch.maximum(torch.zeros_like(nonlinr), nonlinr)
        resp = torch.pow(rectify, 5)

        return resp

    def __init__(self, n_func=8.0, delta=1.0):
        '''
        n_func: number of basis functions
        delta: default sample delta (in degree)
        '''
        self.domain = torch.arange(0, 180.0, delta, dtype=torch.float32)
        self.pref = torch.arange(0, 180.0, 180.0 / n_func, dtype=torch.float32)
        self.beta = None

    def forward(self, stim):
        '''
        Predict voxel responses given stimulus value
        '''
        if self.beta is None:
            raise Exception("Model weights are not yet estimated")

        stim = torch.tensor(stim, dtype=torch.float32)
        resp = self.tuning(stim, self.pref)
        return resp @ self.beta

    def ols(self, stim, voxel):
        '''
        Estimate model weights given stimulus and response
        Stage 1: estimate beta weights using least-square
        '''
        stim = torch.tensor(stim, dtype=torch.float32)
        voxel = torch.tensor(voxel, dtype=torch.float32)

        rgs = self.tuning(stim, self.pref)
        self.beta = torch.linalg.solve(rgs.t() @ rgs, rgs.t() @ voxel.t())

        return self.beta



