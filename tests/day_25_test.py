from solutions.day_25 import parse_raw, part_one, SNAFU

examples = {
    0: "0",
    1: "1",
    2: "2",
    3: "1=",
    4: "1-",
    5: "10",
    6: "11",
    7: "12",
    8: "2=",
    9: "2-",
    10: "20",
    15: "1=0",
    20: "1-0",
    2022: "1=11-2",
    12345: "1-0---0",
    314159265: "1121-1110-1=0",
    1747: "1=-0-2",
    906: "12111",
    198: "2=0=",
    11: "21",
    201: "2=01",
    31: "111",
    1257: "20012",
    32: "112",
    353: "1=-1=",
    107: "1-12",
    7: "12",
    3: "1=",
    37: "122",
}

def test_SNAFU_to_int():
    
    for dec_number, snafu_number in examples.items():
        actual = SNAFU.to_int(snafu_number)
        expected = dec_number
        
        assert actual == expected



def test_int_to_SANFU():
    
    for dec_number, snafu_number in examples.items():
        actual = SNAFU.from_int(dec_number)
        expected = snafu_number
        
        assert actual == expected


def test_part_one():
    example = """1=-0-2
12111
2=0=
21
2=01
111
20012
112
1=-1=
1-12
12
1=
122"""
    snafu_number_list = parse_raw(example)
    
    expected = '2=-1=0'
    actual = part_one(snafu_number_list)
    
    assert actual == expected