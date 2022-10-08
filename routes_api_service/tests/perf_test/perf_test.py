import asyncio
import random
import string
from datetime import datetime
from time import perf_counter

import httpx

from routes_api_service.const import RATES_URL

PORTS = [
    "CNCWN",
    "IESNN",
    "FRLVE",
    "NOOSL",
    "GBPME",
    "NOSVG",
    "FIHEL",
    "NOMAY",
    "FRLIO",
    "SEHAD",
    "GBTIL",
    "DKCPH",
    "NOFRK",
    "CNYAT",
    "CNSNZ",
    "NOSKE",
    "DEWVN",
    "NOKSU",
    "SEMMA",
    "FIRAA",
    "FRDKK",
    "GBLON",
    "NOSVE",
    "FRBAS",
    "NLMOE",
    "IEDUB",
    "FRDPE",
    "FIKOK",
    "NLRTM",
    "GBLTP",
    "BEZEE",
    "FIOUL",
    "NOFUS",
    "FRNEG",
    "DEBRE",
    "SENRK",
    "RUKDT",
    "FRLRH",
    "FIMTY",
    "NOIKR",
    "DKFRC",
    "NOHVI",
    "FRMTX",
    "FIKTK",
    "EEMUG",
    "PLSZZ",
    "NOUME",
    "CNSHK",
    "GBTEE",
    "FRBOD",
    "FRLEH",
    "HKHKG",
    "SESOE",
    "NOHAL",
    "ESGIJ",
    "NOBVG",
    "IEORK",
    "DEBRV",
    "ESZAZ",
    "SEWAL",
    "CNNBO",
    "NOFRO",
    "CNDAL",
    "GBMNC",
    "PLGDY",
    "CNSGH",
    "FITKU",
    "GBHUL",
    "ESVGO",
    "SEHEL",
    "NOMOL",
    "NOTON",
    "CNHDG",
    "BEANR",
    "FIRAU",
    "PLGDN",
    "NODRM",
    "NOSAS",
    "NOKRS",
    "NOSUN",
    "GBBEL",
    "DKAAR",
    "FRURO",
    "GBLGP",
    "SEAHU",
    "NOBVK",
    "FRANT",
    "RUARH",
    "NOTOS",
    "SEGOT",
    "FIIMA",
    "FIKEM",
    "GBGRG",
    "EETLL",
    "FIHMN",
    "RULED",
    "GBLIV",
    "CNGGZ",
    "NOTRD",
    "FRIRK",
    "FRNTE",
    "CNQIN",
    "RULUG",
    "GBBRS",
    "GBGOO",
    "CNLYG",
    "GBTHP",
    "NOHAU",
    "LVRIX",
    "DKAAL",
    "GBFXT",
    "NOMSS",
    "NLAMS",
    "FOTHO",
    "NOHYR",
    "NOTAE",
    "CNTXG",
    "SEGVX",
    "GBSOU",
    "CNXAM",
    "RUULU",
    "NOBGO",
    "ESMPG",
    "DEHAM",
    "SEOXE",
    "NOLAR",
    "CNYTN",
    "ISREY",
    "ESBIO",
    "ISGRT",
    "NOGJM",
    "FRBES",
    "NOORK",
    "NOAES",
    "SESTO",
    "GBIMM",
    "LTKLJ",
    "RUKGD",
    "GBGRK",
    "SEPIT",
    "ESVIT",
    "DKEBJ",
    "GBSSH",
]

REGIONS = [
    "china_main",
    "northern_europe",
    "russia_north_west",
    "north_europe_main",
    "north_europe_sub",
    "china_east_main",
    "china_south_main",
    "baltic",
    "scandinavia",
    "china_north_main",
    "stockholm_area",
    "uk_sub",
    "finland_main",
    "baltic_main",
    "poland_main",
    "kattegat",
    "norway_north_west",
    "norway_south_east",
    "norway_south_west",
    "uk_main",
]


def gen_request_arg(
        ports,
        regions,
        destinations,
        regions_rate=0.1,
        wrong_codes_rate=0.1,
):
    start_date = random.randrange(1, 20)
    end_date = random.randrange(start_date, 30)
    change = random.random()
    if change < wrong_codes_rate:
        a = "".join(random.choices(string.ascii_letters, k=4))
        b = random.choice(destinations)
        origin, destination = (a, b) if random.random() < 0.5 else (b, a)
    elif change < wrong_codes_rate + regions_rate:
        a = random.choice(regions)
        b = random.choice(destinations)
        origin, destination = (a, b) if random.random() < 0.5 else (b, a)
        # There can be the same values, but why not?
    else:
        origin = random.choice(ports)
        destination = random.choice(ports)
        # There can be the same values, but why not?
    return dict(date_from=f"2016-01-{start_date}", date_to=f"2016-01-{end_date}", origin=origin, destination=destination)


async def main(
        url=f"http://127.0.0.1:5000{RATES_URL}",
        ports=PORTS,
        regions=REGIONS,
        regions_rate=0.1,
        wrong_codes_rate=0.1,
        n_requests=1000,
):
    destinations = ports + regions
    test_data = [
        gen_request_arg(ports, regions, destinations, regions_rate, wrong_codes_rate) for _ in range(n_requests)
    ]
    async with httpx.AsyncClient() as client:
        start = perf_counter()
        results = await asyncio.gather(
            *[
                client.get(url, params=t) for t in test_data
            ]
        )
        finish = perf_counter()
        print(f"{n_requests} requests takes {(finish - start) / 1_000} ms")
        n_error = sum(r.status_code != 200 for r in results)
        print(f"Number of errors: {n_error}")


if __name__ == '__main__':
    asyncio.run(main())
