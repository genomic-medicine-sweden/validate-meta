"""Console script for validate_meta."""
import argparse
import sys
from pathlib import Path
import pandas as pd
import yaml
from validate_meta.classes import DataFrameValidator


def main():
    """Console script for validate_meta."""
    parser = argparse.ArgumentParser(prog='validate-meta', description="Validates a GMS-mikro metadata file")

    parser.add_argument("-s", dest="definition", required=True,
                        help="yaml definition file",
                        metavar="DEFINITION YAML FILE")

    group = parser.add_mutually_exclusive_group(required=True)

    group.add_argument("-c", dest="csv",
                        help="csv input file to validate",
                        metavar="CSV FILE")

    group.add_argument("-j", dest="json",
                        help="json file to validate",
                        metavar="JSON FILE")


    args = parser.parse_args()

    csv_file        = Path(args.csv)
    json_file       = Path(args.json)
    definitionfile  = Path(args.definition)
    definition      = None
    df              = None
    dtypes          = None
    errors          = list()

    if definitionfile.exists() and csv_file.exists() or json_file.exists() :
        with definitionfile.open(encoding='utf8') as fp:
            try:
                definition = yaml.safe_load(fp)
                dtypes = {k: v['dtype'] for (k, v) in definition['fields'].items()}
            except Exception as e:
                errors.append("Unable to load yaml field definition file, malformed?")
                errors.append(e)

        if dtypes is not None:
            if csv_file:
                try:
                    df = pd.read_csv(csv_file, dtype=dtypes)
                except Exception as e:
                    errors.append("Unable to load data file. Malformed csv or "
                                  "incorrect dtypes in field definition file?")
                    errors.append(e)
            elif json_file:
                try:
                    df = pd.read_json(json_file, dtype=dtypes)
                except Exception as e:
                    errors.append("Unable to load data file. Malformed json or "
                                  "incorrect dtypes in field definition file?")
                    errors.append(e)

    if definition is not None and df is not None:
        try:
            v = DataFrameValidator(df, definition)
            errors.extend(v.validate())
        except Exception as e:
            errors.append("Unable to validate pandas dataframe. Problems with data (csv or json) "
                          "or field definition yaml?")
            errors.append(e)

    for e in errors:
        print(e)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
