from pipeline.base_logger import logger
import numpy as np
from casacore.tables import table
from pipeline.globals import utils


class MeasurementSet:
    def __init__(self):
        self.measurement_set_path = utils.get_measurement_set_path()
        self.spectral_window_path = self.measurement_set_path + "/SPECTRAL_WINDOW"
        self.measurement_set_data = None
        self.spectral_window_data = None
        logger.debug(f"new measurement set constructed with file path"
                     f": ({self.measurement_set_path})")

    def load_measurement_set(self, readonly=True):
        self.measurement_set_data = table(self.measurement_set_path, readonly=readonly)
        logger.debug(f"measurement set loaded with data from "
                     f"file: ({self.measurement_set_path}) in readonly:{readonly} mode")

    def load_spectral_window(self, readonly=True):
        self.spectral_window_data = table(self.spectral_window_path, readonly=readonly)
        logger.debug(f"spectral window loaded with data from "
                     f"file: ({self.measurement_set_path}) in readonly:{readonly} mode")

    def close_measurement_set(self):
        self.measurement_set_data.close()
        logger.debug(f"measurement set closed")

    def close_spectral_window(self):
        self.spectral_window_data.close()
        logger.debug(f"spectral window closed")

    def get_measurement_set_info(self):
        return self.measurement_set_data.info()

    def get_spectral_window_info(self):
        return self.spectral_window_data.info()

    def get_uv_for_all_frequencies(self):
        u_dist, v_dist, _ = self.measurement_set_data.getcol("UVW").T

        # todo - below code can be optimized
        u_dist_2d = np.transpose(([u_dist] * self.spectral_window_data.getcol("CHAN_FREQ")[0].shape[0]))
        U_all_freqs = (u_dist_2d * (self.spectral_window_data.getcol("CHAN_FREQ")[0] / utils.speed_of_light))

        v_dist_2d = np.transpose(([v_dist] * self.spectral_window_data.getcol("CHAN_FREQ")[0].shape[0]))
        V_all_freqs = (v_dist_2d * (self.spectral_window_data.getcol("CHAN_FREQ")[0] / utils.speed_of_light))

        return U_all_freqs, V_all_freqs