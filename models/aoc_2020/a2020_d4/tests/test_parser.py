from models.common.io import InputFromString
from ..parser import parse_passports


def test_parse_passport():
    file_content = """
                   ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
                   byr:1937 iyr:2017 cid:147 hgt:183cm

                   hcl:#ae17e1 iyr:2013
                   eyr:2024
                   ecl:brn pid:760753108 byr:1931
                   hgt:179cm
                   """
    passports = list(parse_passports(InputFromString(file_content)))
    assert passports == [
        {
            "ecl": "gry",
            "pid": "860033327",
            "eyr": "2020",
            "hcl": "#fffffd",
            "byr": "1937",
            "iyr": "2017",
            "cid": "147",
            "hgt": "183cm",
        },
        {
            "hcl": "#ae17e1",
            "iyr": "2013",
            "eyr": "2024",
            "ecl": "brn",
            "pid": "760753108",
            "byr": "1931",
            "hgt": "179cm",
        },
    ]
