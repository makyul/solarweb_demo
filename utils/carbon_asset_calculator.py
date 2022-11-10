"""
Perform various carbon asset burning process calculations.

"""

import csv

from geopy.geocoders import Nominatim
from logging import getLogger

from .constants import CO2_INTENSITY_TABLE_PATH, WORLD_CO2_INTENSITY

logger = getLogger(__name__)


def get_tokens_to_burn(kwh: float, geo: str) -> float:
    """
    Get an amount of carbon assets to burn based on a number of kWt*h burnt and country of residence.
        Source:
        CO2 emission intensity by countries: https://ourworldindata.org/electricity-mix#carbon-intensity-of-electricity

        DISCLAIMER: THIS IS NOT INTENDED TO BE A COMPLETELY ACCURATE CALCULATION. THE FINAL RESULT HEAVILY DEPENDS ON
        THE TYPE OF COAL USED. ALSO, THE STATISTICS DATA MAY BE INCORRECT/OUTDATED. THEREFORE, DO NOT TREAT THIS AS
        A SCIENTIFIC RESEARCH.

    :param kwh: Number of kWt*h to compensate.
    :param geo: Coordinates of the household.

    :return: Number of carbon assets to burn.

    """
    co2_intensity: float = WORLD_CO2_INTENSITY

    logger.info(f"Getting country by geo: {geo}.")
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.reverse(geo, language="en")
    if location:
        country: str = location.raw["address"]["country"]
        logger.info(f"Country based on geo: {country}.")

        logger.info(f"Getting CO2 intensity in g/kWh for {country}.")
        with open(CO2_INTENSITY_TABLE_PATH, "r") as intensity:
            intensity_csv = csv.reader(intensity)
            for row in intensity_csv:
                if row[0] == country:
                    co2_intensity = float(row[1])
                    break
        logger.info(f"CO2 intensity for {country}: {co2_intensity} g/kWh.")

    else:
        logger.info(f"No country was determined. Using global coefficient: {WORLD_CO2_INTENSITY} g/kWh.")

    tons_co2 = kwh * co2_intensity / 10**6  # Table shows how many grams of CO2 produced per kWh generated in country.

    logger.info(f"Number of metric tons of CO2 / Carbon assets to burn for {kwh} kWh: {tons_co2}.")

    return tons_co2  # 1 Carbon asset per metric tonn of co2
