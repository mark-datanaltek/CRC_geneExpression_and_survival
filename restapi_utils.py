import json
from math import ceil
from pathlib import Path
from typing import Dict, List
import requests
from time import sleep

def get_probeset_json(probesets: List[str], chunksize=30, datfile="probesets.json") -> List[Dict]:
# use the ensemble REST-API to get annotations for all the probes in the dataset
# IF we don't already have it saved to disk.  The full API call takes ~37 min!
    probeset_jsons = None
    if Path(datfile).is_file():
        # if datfile exists read it for the data
        with open(datfile, 'r') as f_in:
            probeset_jsons = json.load(f_in)
        
        # confirm that we have the right probesets
        probesets_found = [probeset["name"] for probeset in probeset_jsons]
        err_msg = f"probesets_found IS NOT EQUAL TO probeset.\n" + \
                  f"{probesets_found[0]} {probesets[0]}\n" + \
                  f"{probesets_found[1]} {probesets[1]}\n" + \
                  f"{probesets_found[2]} {probesets[2]}\n"
        assert sorted(probesets_found) == sorted(probesets), err_msg

    else:
        # the datfile doesn't exist, so we get the data from the REST-API
        probeset_jsons = []
        server: str = "https://rest.ensembl.org"
        ext_pt1: str = "/regulatory/species/homo_sapiens/microarray/HG-U133_Plus_2/probe_set/"

        num_chunks: int = ceil(len(probesets) / chunksize)
        for chunknum in range(num_chunks):
            print(f"calling REST-API for chunknum {chunknum}")
            for probeset in probesets[chunknum*chunksize:(chunknum+1)*chunksize]:
                ext_pt2: str = f"{probeset}?gene=1;transcript=1"
                response: requests.Response = requests.get(server+ext_pt1+ext_pt2, headers={"Content-Type":"application/json"})
                if not response.ok:
                    print(f"response.ok IS NOT TRUE for probeset:{probeset}")
                    response.raise_for_status()
                probeset_jsons.append(response.json())
            sleep(3)

    return probeset_jsons