"""Execute every code cell using a standard local Jupyter kernel."""
from pathlib import Path
import json, time
import nbformat
from nbclient import NotebookClient

root=Path(__file__).resolve().parents[1]
path=root/"crypto_eda_2026_forecasts.ipynb"
nb=nbformat.read(path,as_version=4)
start=time.time()
client=NotebookClient(nb,timeout=600,kernel_name="python3",resources={"metadata":{"path":str(root)}})
client.execute()
nbformat.validate(nb)
nbformat.write(nb,path)
report={"execution_engine":"Jupyter kernel via nbclient","executed_code_cells":sum(c.cell_type=="code" and c.execution_count is not None for c in nb.cells),
        "total_code_cells":sum(c.cell_type=="code" for c in nb.cells),"errors":[],"runtime_seconds":round(time.time()-start,2),
        "plotly_outputs":sum("application/vnd.plotly.v1+json" in o.get("data",{}) for c in nb.cells for o in c.get("outputs",[])),
        "png_outputs":sum("image/png" in o.get("data",{}) for c in nb.cells for o in c.get("outputs",[]))}
(root/"results/execution_report.json").write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
