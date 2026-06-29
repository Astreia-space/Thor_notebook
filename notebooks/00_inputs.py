"""00 — Input spreadsheet: edit data/inputs/thor_inputs.csv (all THOR numbers)."""

import marimo

__generated_with = "0.10.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import polars as pl

    from thor.io.inputs import INPUTS_CSV, load_inputs, section_table
    return INPUTS_CSV, load_inputs, mo, pl, section_table


@app.cell
def _(INPUTS_CSV, mo):
    mo.md(f"""
    # THOR Inputs (planilha central)

    **Edite os números aqui:** `{INPUTS_CSV}`

    | Coluna | Significado |
    |--------|-------------|
    | `section` | Grupo (mission, phase, mass, orbit, entry, …) |
    | `item` | Linha dentro do grupo (vazio = parâmetro global) |
    | `parameter` | Nome do campo |
    | `value` | **Valor numérico ou texto** |
    | `unit` | Unidade (referência) |
    | `notes` | Comentário |

    Depois reexecute os notebooks downstream (`00_mission_conops` → …).
    """)
    return


@app.cell
def _(load_inputs, mo):
    inputs = load_inputs()
    mo.ui.table(inputs)
    return (inputs,)


@app.cell
def _(inputs, mo, section_table):
    sections = inputs["section"].unique().sort().to_list()
    mo.accordion({f"{s} ({len(section_table(s))} rows)": mo.ui.table(section_table(s)) for s in sections})
    return (sections,)


if __name__ == "__main__":
    app.run()
