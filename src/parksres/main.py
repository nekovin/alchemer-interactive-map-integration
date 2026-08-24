import argparse
import sys
from collections.abc import Sequence

def main(argv: Sequence[str] | None=None) -> None:
    parser = argparse.ArgumentParser(
        description=""
    )

    _args = parser.parse_args(argv)
    
    if not sys.argv[1:]:
        from parksres import gdb_to_json, build_parks_vic, add_centres
        from parksres.scripts import map_metro_data, map_types
        gdb_to_json.main()
        map_metro_data.main(["--save"])
        map_types.main()
        build_parks_vic.main(["-a"])
        add_centres.main()

if __name__ == '__main__':
    main()