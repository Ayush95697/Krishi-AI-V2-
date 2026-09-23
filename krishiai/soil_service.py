"""
KrishiAI+ — Soil Interpretation Module

Rule-based (not ML-trained) interpreter for real, farmer-provided soil test values.
This module deliberately does NOT infer anything from GPS/location — every rating
is computed only from measured soil parameters the farmer actually provides, per
the project's response to the "soil varies within a field" scientific-rigor concern.

SOURCES (two distinct source families — do not blend without citing both):

  Family 1 — N, P, K, OC, S, B, pH:
    "Methods Manual - Soil Testing in India", Department of Agriculture &
    Cooperation, Ministry of Agriculture, Government of India, Jan 2011.
      - N / P (Olsen) / K / OC: Table 1, p.34
      - pH classes: Table 14, p.79
      - S, B: Soil Health Card 2014-15 Operational Guidelines, sample card annex

  Family 2 — Zn, Fe, Mn, Cu:
    Lindsay, W.L. & Norvell, W.A. (1978). "Development of a DTPA soil test for
    zinc, iron, manganese, and copper." Soil Science Society of America Journal.
    (DTPA-extractable critical deficiency limits.)

NOTE ON STATE VARIATION: Some states (e.g. TNAU) use different N/P cutoffs than
the central GoI manual (e.g. TNAU: N 240/480 vs this manual's 280/560). This
module intentionally follows ONE scheme (the central GoI manual) throughout and
states that choice explicitly, rather than silently mixing regional standards.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ParameterRating:
    parameter: str
    value: float
    unit: str
    rating: str          # "Low" / "Medium" / "High" (or acidity/alkalinity class for pH)
    source: str
    note: Optional[str] = None


def _band(value, low_max, high_min, low_label="Low", mid_label="Medium", high_label="High"):
    if value < low_max:
        return low_label
    elif value <= high_min:
        return mid_label
    else:
        return high_label


def rate_nitrogen(n_kg_ha: float) -> ParameterRating:
    rating = _band(n_kg_ha, 280, 560)
    return ParameterRating("Nitrogen (N)", n_kg_ha, "kg/ha", rating,
                            "GoI Methods Manual (2011), Table 1, p.34")


def rate_phosphorus(p_kg_ha: float) -> ParameterRating:
    rating = _band(p_kg_ha, 10, 24.6)
    return ParameterRating("Phosphorus (P, Olsen)", p_kg_ha, "kg/ha", rating,
                            "GoI Methods Manual (2011), Table 1, p.34")


def rate_potassium(k_kg_ha: float) -> ParameterRating:
    rating = _band(k_kg_ha, 108, 280)
    return ParameterRating("Potassium (K)", k_kg_ha, "kg/ha", rating,
                            "GoI Methods Manual (2011), Table 1, p.34")


def rate_organic_carbon(oc_percent: float) -> ParameterRating:
    rating = _band(oc_percent, 0.5, 0.75)
    return ParameterRating("Organic Carbon (OC)", oc_percent, "%", rating,
                            "GoI Methods Manual (2011), Table 1, p.34")


def rate_sulphur(s_ppm: float) -> ParameterRating:
    rating = _band(s_ppm, 10, 20)
    return ParameterRating("Sulphur (S)", s_ppm, "ppm", rating,
                            "SHC 2014-15 Operational Guidelines, card annex")


def rate_boron(b_ppm: float) -> ParameterRating:
    rating = "Low" if b_ppm < 0.5 else "High"
    return ParameterRating("Boron (B)", b_ppm, "ppm", rating,
                            "SHC 2014-15 Operational Guidelines, card annex",
                            note="Card template uses a single cutoff (no separate Medium band).")


def rate_ph(ph: float) -> ParameterRating:
    if ph < 4.6:
        rating = "Extremely acid"
    elif ph < 5.6:
        rating = "Strongly acid"
    elif ph < 6.6:
        rating = "Moderately acid"
    elif ph < 7.0:
        rating = "Slightly acid"
    elif ph == 7.0:
        rating = "Neutral"
    elif ph <= 8.5:
        rating = "Moderately alkaline"
    else:
        rating = "Strongly alkaline"
    return ParameterRating("pH", ph, "", rating,
                            "GoI Methods Manual (2011), Table 14, p.79")


def rate_ec(ec_dsm: float) -> ParameterRating:
    if ec_dsm < 1:
        rating = "Normal (non-saline)"
    elif ec_dsm < 2:
        rating = "Slightly saline"
    elif ec_dsm < 4:
        rating = "Moderately saline"
    elif ec_dsm < 8:
        rating = "Saline"
    else:
        rating = "Highly saline"
    return ParameterRating("Electrical Conductivity (EC)", ec_dsm, "dS/m", rating,
                            "Richards (1954) / USDA salinity classification",
                            note="Standard irrigation-agriculture salinity scale, not GoI-manual sourced.")


def rate_micronutrient(name: str, value_ppm: float, critical_limit: float) -> ParameterRating:
    rating = "Deficient" if value_ppm < critical_limit else "Sufficient"
    return ParameterRating(name, value_ppm, "ppm", rating,
                            "Lindsay & Norvell (1978), DTPA critical limits")


def rate_zinc(zn_ppm: float) -> ParameterRating:
    return rate_micronutrient("Zinc (Zn)", zn_ppm, 0.6)


def rate_iron(fe_ppm: float) -> ParameterRating:
    return rate_micronutrient("Iron (Fe)", fe_ppm, 4.5)


def rate_manganese(mn_ppm: float) -> ParameterRating:
    return rate_micronutrient("Manganese (Mn)", mn_ppm, 1.0)


def rate_copper(cu_ppm: float) -> ParameterRating:
    return rate_micronutrient("Copper (Cu)", cu_ppm, 0.2)


def interpret_soil(
    n_kg_ha: float,
    p_kg_ha: float,
    k_kg_ha: float,
    oc_percent: float,
    ph: float,
    ec_dsm: Optional[float] = None,
    s_ppm: Optional[float] = None,
    b_ppm: Optional[float] = None,
    zn_ppm: Optional[float] = None,
    fe_ppm: Optional[float] = None,
    mn_ppm: Optional[float] = None,
    cu_ppm: Optional[float] = None,
) -> dict:
    """
    Interprets a real, farmer-provided soil test report.

    Only N, P, K, OC, and pH are required — these are the parameters every
    Soil Health Card reports. EC, S, B, and the four micronutrients are
    optional, since not every card/lab reports all 12 parameters.

    Returns a dict of {parameter_key: ParameterRating} plus a plain-language
    summary list of any Low/deficient/problematic findings, and a disclaimer
    field that must be surfaced to the farmer, not silently dropped.
    """
    results = {
        "nitrogen": rate_nitrogen(n_kg_ha),
        "phosphorus": rate_phosphorus(p_kg_ha),
        "potassium": rate_potassium(k_kg_ha),
        "organic_carbon": rate_organic_carbon(oc_percent),
        "ph": rate_ph(ph),
    }
    if ec_dsm is not None:
        results["ec"] = rate_ec(ec_dsm)
    if s_ppm is not None:
        results["sulphur"] = rate_sulphur(s_ppm)
    if b_ppm is not None:
        results["boron"] = rate_boron(b_ppm)
    if zn_ppm is not None:
        results["zinc"] = rate_zinc(zn_ppm)
    if fe_ppm is not None:
        results["iron"] = rate_iron(fe_ppm)
    if mn_ppm is not None:
        results["manganese"] = rate_manganese(mn_ppm)
    if cu_ppm is not None:
        results["copper"] = rate_copper(cu_ppm)

    concerns = []
    for key, r in results.items():
        if r.rating in ("Low", "Deficient", "Extremely acid", "Strongly acid",
                         "Strongly alkaline", "Saline", "Highly saline"):
            concerns.append(f"{r.parameter}: {r.rating} ({r.value} {r.unit})")

    return {
        "ratings": {k: vars(v) for k, v in results.items()},
        "concerns": concerns,
        "disclaimer": (
            "Interpreted from measured soil test values only — this system does not "
            "infer soil health from location, since soil composition varies "
            "significantly even within a single field. Thresholds follow the GoI "
            "Methods Manual (2011) and Lindsay & Norvell (1978); other schemes "
            "(e.g. TNAU) may classify the same values differently."
        ),
    }
