import argparse
from firecloud import api as fapi


def main(argv):
    parser = argparse.ArgumentParser(
        description="Export workspace storage cost estimates associated with the user to TSV"
    )
    parser.add_argument("--output", help="Output TSV path", required=True)
    parser.add_argument(
        "--access",
        help="Workspace access levels",
        choices=["owner", "reader", "writer"],
        action="append",
    )
    args = parser.parse_args(argv)

    workspaces = fapi.list_workspaces().json()

    access = args.access
    if access is None:
        access = []
    output = args.output
    access_filter = set()
    if "reader" in access:
        access_filter.add("READER")
    if "writer" in access:
        access_filter.add("WRITER")
    if "owner" in access or len(access) == 0:
        access_filter.add("OWNER")

    with open(output, "wt") as out:
        out.write("namespace\tname\testimate\n")
        for w in workspaces:
            if w["accessLevel"] in access_filter:
                namespace = w["workspace"]["namespace"]
                name = w["workspace"]["name"]

                # Use the updated API method
                r = fapi.get_storage_cost(namespace, name)
                if r.status_code == 200:
                    estimate = r.json()["estimate"]
                    out.write(f"{namespace}\t{name}\t{estimate}\n")
                else:
                    print(f"Warning: Could not get storage cost for {namespace}/{name}: {r.status_code}")
