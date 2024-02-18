import resdk
from resdk.tables import RNATables
import decoupler
import pandas as pd
from typing import Optional, Tuple
import argparse


def get_data(collection_name: str) -> Optional[Tuple[pd.DataFrame, str]]:
    """
    Retrieves dataset with specified name and preprocesses it.
    :param collection_name: Name of the collection
    :return: If all actions are successful, returns a tuple with:
                pandas DataFrame with dataset (samples x genes)
                species the samples were collected from.
             Otherwise, returns None.
    """
    try:
        res = resdk.Resolwe(url='https://app.genialis.com')
    except Exception as e:
        print("There was a problem connecting to the Genialis Expressions data repository. Please try again later.")
        print(e)
        return None

    try:
        # Try to find the selected collection
        collection = res.collection.get(collection_name)
        table = RNATables(collection)

        # Check if selected dataset is in TPM format
        if table.exp.attrs["exp_type"] != "TPM":
            print(f"Selected dataset is not in 'TPM' format. Please select another dataset.")

    except LookupError:
        print(f"Collection named '{collection_name}' does not exist.\nPlease select an existing dataset name.")
        return None

    # Change columns and rows to readable values
    table.exp.columns = table.exp.columns.astype(str)
    exp = table.exp.rename(columns=table.readable_columns, index=table.readable_index)

    # Assume all samples in collection are taken from the same species
    species = collection.samples[0].get_annotation("general.species").value

    return exp, species


def calculate_progeny(g_mtx: pd.DataFrame, species: str) -> Optional[pd.DataFrame]:
    """
    Retrieves PROGENy matrix for given species and calculates Pathway score P from given gene expression matrix.
    The Pathway score P is calculated as described by Schubert et al. 2018 and normalized.
    :param g_mtx: Gene expression matrix (samples x genes)
    :param species:
    :return: DataFrame with PROGENy scores (samples x pathways)
    """

    try:
        # By default get top 100 genes per pathway
        prog = decoupler.get_progeny(species)
    except Exception as e:
        print(f"There was a problem getting PROGENy matrix for {species}.\nPlease try another dataset with samples from "
              f"'Homo sapiens'.")
        print(e)
        return None

    # Transform Dataframe in long format to matrix that can be used for multiplication.
    pathways, samples, mtx = decoupler.get_net_mat(prog)
    prog_mtx = pd.DataFrame(mtx, index=samples, columns=pathways)

    # Get genes that appear both in Gene expression matrix and PROGENy matrix
    matching = [i for i in prog_mtx.index.values if i in g_mtx.columns]

    # Matrix multiplication
    P = g_mtx[matching].dot(prog_mtx.loc[matching])

    # Normalize to get mean of 0 and std of 1
    P_norm = P.apply(lambda x: (x - x.mean()) / x.std(), axis=1)

    return P_norm


def print_results(progeny_score: pd.DataFrame, collection_name: str, output_file=False):
    """
    Prints out formatted table of PROGENy scores for each sample and saves it to output_file
    :param progeny_score: DataFrame (samples x pathways)
    :param collection_name: Name of collection
    :param output_file: if true, output Markdown file is created
    :return:
    """

    print(f"\nNormalized PROGENy scores for samples in collection '{collection_name}':\n")
    result_table = progeny_score.to_markdown()
    print(result_table)

    if output_file:
        with open(f"{collection_name}_progeny.md", "w+") as f:
            f.write(result_table)


def main():

    # Parse the arguments
    parser = argparse.ArgumentParser(
        prog="progeny",
        description="Get PROGENy scores for selected collection.")
    parser.add_argument("collection_name", type=str, help="name of collection")
    parser.add_argument("-o", dest="output_file", action="store_true",
                        help="if selected, create an output Markdown file")

    parser.set_defaults(output_file=False)

    args = parser.parse_args()

    collection_name = args.collection_name

    data = get_data(collection_name)
    if data is not None:
        mat, species = data
        print(f"\nSuccessfully retrieved dataset '{collection_name}' with {mat.shape[0]} samples and {mat.shape[1]} genes "
              f"from '{species}'.")

        P = calculate_progeny(mat, species)

        print_results(P, collection_name, args.output_file)


if __name__ == "__main__":
    main()
