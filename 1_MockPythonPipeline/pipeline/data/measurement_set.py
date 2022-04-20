import numpy as np
from typing import List
from pipeline.utilities.base_logger import logger
from casacore.tables import table
from pipeline.catalog.catalog import Source, Coordinates
from pipeline.utilities.globals import utils


class MeasurementSet:
    def __init__(self):
        self.measurement_set_path = utils.get_measurement_set_path()
        self.spectral_window_path = self.measurement_set_path + "/SPECTRAL_WINDOW"
        self.measurement_set_data = None
        self.spectral_window_data = None
        self.u_all_frequencies = None
        self.v_all_frequencies = None
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
        frequencies = self.spectral_window_data.getcol("CHAN_FREQ")[0]
        number_frequency_bands = frequencies.shape[0]

        # todo - below code can be optimized
        u_dist_2d = np.transpose(([u_dist] * number_frequency_bands))
        u = (u_dist_2d * (frequencies / utils.speed_of_light))

        v_dist_2d = np.transpose(([v_dist] * number_frequency_bands))
        v = (v_dist_2d * (frequencies / utils.speed_of_light))

        logger.info(f"u,v computed for all {number_frequency_bands} frequency bands")
        self.u_all_frequencies = u
        self.v_all_frequencies = v
        return u, v

    def simulate_sources(self, sources: List[Source]):
        simulated_data_with_polarization = np.zeros(
            (self.u_all_frequencies.shape[0], self.u_all_frequencies.shape[1], 4))
        for source in sources:
            l, m = source.get_coordinates().radec2lm(Coordinates(utils.phase_center_str, frame="fk5"))
            simulated_data = np.exp(1j * 2 * np.pi *
                                    (l * self.u_all_frequencies
                                     + m * self.v_all_frequencies))  # todo - include brightness
            simulated_data_with_polarization = simulated_data_with_polarization + \
                                               np.repeat(simulated_data[:, :, np.newaxis], 4, axis=2)
        simulated_data_with_polarization[:, :, 1:3] = 0
        logger.info(f"simulated data for all {len(sources)} sources")

        return simulated_data_with_polarization

    def update_corrected_data_column(self, simulated_data):
        self.measurement_set_data.close()
        self.load_measurement_set(readonly=False)
        self.measurement_set_data.putcol("CORRECTED_DATA", simulated_data)
        self.measurement_set_data.close()
        logger.info(f"simulated sources saved to file: {self.measurement_set_path}")
