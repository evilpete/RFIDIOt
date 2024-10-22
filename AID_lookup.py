#!/usr/bin/env python3

from typing import Tuple
try:
    from AID_data import AID_DAT
except ImportError as _e:
    print(f'Failed to import AID data file "AID_data.py": {_e}')
    AID_DAT = {}
    # sys.exit(0)
# import pprint

_verbose = 1


class AID_Lookup():

    def __init__(self, debug=False):
        self.aid_dat = AID_DAT
        self.debug = debug
        if debug:
            print(f"AID DATA: {len(self.aid_dat)} entries")

    # lookup AID in self.aid_dat,
    # if not found look up substring / registered application provider identifier (RID)
    def lookup(self, aid: str = None) -> Tuple[str, str]:

        # if there's nothing to report
        if aid is None or not self.aid_dat:
            return "", ""

        dat = None
        while len(aid) >= 10:
            if self.debug:
                print(len(aid), "trying", aid)
            if aid in self.aid_dat:
                dat = self.aid_dat[aid]
                break
            if len(aid) == 14:
                aid = aid[:10]
            else:
                aid = aid[:-1]

        if dat:
            # print([f"{x}:{y}" for x, y in enumerate(dat)])
            if dat[0]:
                aid_info = f"{dat[0]} {dat[2]}"
            else:
                aid_info = f"{dat[2] or dat[1]} {dat[4]}"
            return aid, aid_info

        return "", ""

    def self_test(self) -> bool:

        if not self.aid_dat:
            print(f"No AID Data / AID Data Missing")
            return False

        ret_val = True

        test_AIDs = [
            "A0000005272001", "A000000527200101",
        ]

        # Print found item
        for t_aid in test_AIDs:
            aid_found, aid_description = self.lookup(t_aid)

            if not aid_found:
                print(f"{t_aid}: Not Found / Unknown")
                ret_val = False
                continue

            if self.debug:
                print(f"{t_aid}:\n\t{aid_found + ':':22s} {aid_description}")

        return ret_val

# test AIDs,  Most are real, some with good RID but unknown/bad PIX
# See
#     https://www.eftlab.com/knowledge-base/complete-list-of-application-identifiers-aid
#     https://en.wikipedia.org/wiki/EMV#Application_selection


if __name__ == '__main__':

    aid_lookup = AID_Lookup(debug=False)

    if aid_lookup.self_test():
        print("Self test: Pass")
    else:
        print("Self test: Fail")
