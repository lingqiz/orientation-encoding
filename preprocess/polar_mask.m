function mask = polar_mask(angle, polarLo, polarHi)
mask = ((angle >= polarLo) & (angle < polarHi)) | ((angle >= polarLo + 180) & (angle < polarHi + 180));
end