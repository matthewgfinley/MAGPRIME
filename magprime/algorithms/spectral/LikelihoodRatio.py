# ╔══════════════════════════════════════════════════════════════════════════════╗
# ║              █ █ █ █ █   MAGPRIME Toolkit   █ █ █ █ █                        ║
# ║ ──────────────────────────────────────────────────────────────────────────── ║
# ║  Module       :  LikelihoodRatio.py                                          ║
# ║  Package      :  magprime                                                    ║
# ║  Author       :  Dr. Matthew G. Finley  <matthew.g.finley@nasa.gov>          ║
# ║  Affiliation  :  NASA Goddard Space Flight Center — Greenbelt, MD 20771      ║
# ║  Created      :  2025-05-21                                                  ║
# ║  Last Updated :  2025-05-22                                                  ║
# ║  Python       :  ≥ 3.10                                                      ║
# ║  License      :  MIT — see LICENSE.txt                                       ║
# ║                                                                              ║
# ║  Description  : Implementation of a likelihood ratio-based method of         ║
# ║  spectral track detection. Methodology originally described in'An Image      ║
# ║  Processing Approach to Frequency Tracking (Application to Sonar Data)' by   ║
# ║  Abel et al., 1992 IEE International Conference on Acoustics, Speech,        ║
# ║  and Signal Processing (1992).                                               ║
# ╚══════════════════════════════════════════════════════════════════════════════╝

import numpy as np
from scipy.stats import trim_mean
from scipy.ndimage import uniform_filter1d, median_filter

def likelihood_ratio(s, threshold=3):
    broadband_s = np.zeros(np.shape(s))
    narrowband_s = np.zeros(np.shape(s))
    for i in range(np.shape(s)[1]):
        raw_spectrum = s[:,i]
        broadband_spectrum = uniform_filter1d(raw_spectrum, 10)
        narrowband_spectrum = raw_spectrum - broadband_spectrum
        narrowband_spectrum = narrowband_spectrum - trim_mean(narrowband_spectrum, 0.10)

        broadband_s[:,i] = broadband_spectrum
        narrowband_s[:,i] = narrowband_spectrum

    SNR_ij = narrowband_s / broadband_s
    SNR_ij_p1 = SNR_ij + np.ones(np.shape(SNR_ij))
    Sb_ij = broadband_s

    test_statistic = (SNR_ij / SNR_ij_p1) * (s / Sb_ij)

    detected_pixels = (test_statistic > threshold).astype(np.uint8)

    median_filtered_detections = median_filter(detected_pixels, (1,3))

    return median_filtered_detections