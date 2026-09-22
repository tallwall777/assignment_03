"""
process_file.py — Part 2: one file of package descriptions, uploaded.

A Streamlit app that accepts an uploaded text file with one package description
per line, shows the total for every line, and writes the parsed packages to a
JSON file in the `data/` folder — `data/packaging1.txt` in, `data/packaging1.json`
out.

New here: an uploaded file arrives as **bytes**, not text, so it has to be
decoded before it can be split into lines. And a text file usually ends with a
newline, so the last "line" is empty and must be skipped rather than parsed.

Run it:  Run and Debug -> "Streamlit Run: Current File"   (see README Reference #1)
Test it: pytest tests/test_streamlit.py -k process_file
"""

# --- The page ---------------------------------------------------------------------
#
# Less scaffolding this time. The steps are described, but which widget and which
# function does each job — and what to call the result — is now yours to work out.
# `one_package.py` is your worked example for anything structural, and README
# Reference #4 and #5 cover the two things that are new here.

import json

import streamlit as st

from packaging_parser import calc_total_units, get_unit, parse_packaging

st.title("Process File of Packages")

package_file = st.file_uploader("Upload a packaging file", key="package_file")

packages = []
out_path = ""

if package_file:
    text = package_file.read().decode("utf-8")
    lines = text.splitlines()

    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue

        package = parse_packaging(stripped)
        total = calc_total_units(package)
        unit = get_unit(package)

        packages.append(package)
        st.info(f"{stripped} ➡️ Total 📦 Size: {total} {unit}")

    out_name = package_file.name.replace(".txt", ".json")
    out_path = f"data/{out_name}"
    with open(out_path, "w", encoding="utf-8") as file_handle:
        json.dump(packages, file_handle)

    st.success(f"{len(packages)} packages written to {out_path}")
