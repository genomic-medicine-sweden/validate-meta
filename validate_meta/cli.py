"""Console script for validate_meta."""
import argparse
import sys
from pathlib import Path
import pandas as pd
import yaml
from validate_meta.classes import DataFrameValidator


def main():
    """Console script for validate_meta."""
    parser = argparse.ArgumentParser(description="Validates a GMS-mikro metadata file")
    parser.add_argument("-i", dest="filename", required=True,
                        help="input file with two matrices",
                        metavar="CSV DATA FILE")

    parser.add_argument("-s", dest="definition", required=True,
                        help="yaml definition file",
                        metavar="DEFINITION YAML FILE")

    args = parser.parse_args()

    datafile        = Path(args.filename)
    definitionfile  = Path(args.definition)
    definition      = None
    df              = None
    dtypes          = None
    errors          = list()

    if datafile.exists() and definitionfile.exists():
        with definitionfile.open(encoding='utf8') as fp:
            try:
                definition = yaml.safe_load(fp)
                dtypes = {k: v['dtype'] for (k, v) in definition['fields'].items()}
            except Exception as e:
                errors.append("Unable to load yaml field definition file, malformed?")
                errors.append(e)

        if dtypes is not None:
            try:
                df = pd.read_csv(datafile, dtype=dtypes)
            except Exception as e:
                errors.append("Unable to load data file. Malformed data csv "
                              "or incorrect dtypes in field definition file?")
                errors.append(e)


    if definition is not None and df is not None:
        try:
            v = DataFrameValidator(df, definition)
            errors.extend(v.validate())
        except Exception as e:
            errors.append("Unable to validate pandas dataframe. Problems with data csv or field definition yaml?")
            errors.append(e)

    for e in errors:
        print(e)

    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
