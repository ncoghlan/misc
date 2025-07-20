import marimo

__generated_with = "0.14.12"
app = marimo.App()


@app.cell
def _():
    import datetime
    import pandas
    import pathlib
    from email.parser import HeaderParser
    return HeaderParser, datetime, pandas, pathlib


@app.cell
def _(HeaderParser, datetime, pathlib):
    PEP_DIR = pathlib.Path.home() / "devel/peps"
    _header_parser = HeaderParser()
    print(datetime.datetime.utcnow())
    return (PEP_DIR,)


@app.cell
def _(PEP_DIR, pandas):
    import re
    def _get_names_for_field(value):
        # Gets a list of names for the BDFL-Delegate or Author field
        lines = value.splitlines()
        entries = []
        for line in lines:
            entries.extend(line.split(","))
        names = []
        for entry in entries:
            entry = entry.strip().strip(',').strip()
            # Strip "name <email address>" email addresses
            entry = re.sub(" <.*?>", "", entry)
            # Strip "email address (name)" email addresses
            entry = re.sub(r"[^@]+?@.*? \((.*?)\)", r"\1", entry)
            if entry:
                names.append(entry)
        return names

    def extract_headers(pep):   
        headers = {field.lower().replace("-", "_"):value for field, value in pep.items()}
        # First normalise BDFL delegate, and handle co-delegates
        bdfl_delegate = headers.get("bdfl_delegate")
        headers_by_bdfl_delegate = []
        if bdfl_delegate is not None:
            delegate_names = _get_names_for_field(bdfl_delegate)
            for delegate in delegate_names:
                delegate_headers = headers.copy()
                delegate_headers["bdfl_delegate"] = delegate
                headers_by_bdfl_delegate.append(delegate_headers)
        else:
            headers_by_bdfl_delegate.append(headers)
        
        authors = _get_names_for_field(headers["author"])
        headers_by_author = []
        for delegate_headers in headers_by_bdfl_delegate:
            for author in authors:
                author_headers = delegate_headers.copy()
                author_headers["author"] = author
                headers_by_author.append(author_headers)
        return headers_by_author

    # With credit to http://beneathdata.com/how-to/email-behavior-analysis/
    pep_headers = [_header_parser.parse(pep.open()) for pep in PEP_DIR.glob("*.txt") if not pep.name.endswith("0000.txt")]
    all_peps = pandas.DataFrame(header_set for pep in pep_headers for header_set in extract_headers(pep))
    final_or_active_peps = all_peps.query("status in ['Final', 'Active']")
    return all_peps, final_or_active_peps


@app.cell
def _(all_peps):
    def print_metrics(pep_data, prefix = "All"):
        print(prefix + " PEPs:", pep_data.pep.nunique())
        print(prefix + " PEPs authored or co-authored by Guido:", pep_data.author.value_counts()["Guido van Rossum"])
        print(prefix + " PEPs authored or co-authored by me:", pep_data.author.value_counts()["Nick Coghlan"])
        with_delegate = pep_data[pep_data["bdfl_delegate"].notnull()]
        print(prefix + " PEPs with BDFL-Delegate:", with_delegate.pep.nunique())
        print(prefix + " PEPs delegated to me:", with_delegate.bdfl_delegate.value_counts()["Nick Coghlan"])

    print_metrics(all_peps)
    return (print_metrics,)


@app.cell
def _(final_or_active_peps, print_metrics):
    print_metrics(final_or_active_peps, "Final or Active")
    return


@app.cell
def _(all_peps):
    has_bdfl_delegate = all_peps["bdfl_delegate"].notnull()
    all_peps[has_bdfl_delegate].bdfl_delegate.value_counts()
    return


@app.cell
def _(final_or_active_peps):
    final_or_active_peps.author.value_counts()
    return


@app.cell
def _(all_peps):
    withdrawn_or_deferred_peps = all_peps.query("status in ['Withdrawn', 'Deferred']")
    return (withdrawn_or_deferred_peps,)


@app.cell
def _(withdrawn_or_deferred_peps):
    withdrawn_or_deferred_peps.author.value_counts()
    return


if __name__ == "__main__":
    app.run()
