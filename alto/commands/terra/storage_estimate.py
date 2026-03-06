import argparse
from datetime import datetime
from firecloud import api as fapi


HTML_TEMPLATE = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Terra Workspace Storage Cost Report</title>
    <link rel="stylesheet" href="https://cdn.datatables.net/1.13.7/css/jquery.dataTables.min.css">
    <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
    <script src="https://cdn.datatables.net/1.13.7/js/jquery.dataTables.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background-color: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 3px solid #4285f4;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #333;
            margin-top: 30px;
            margin-bottom: 15px;
        }}
        .summary {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}
        .summary-item {{
            text-align: center;
        }}
        .summary-value {{
            font-size: 2em;
            font-weight: bold;
            color: #4285f4;
        }}
        .summary-label {{
            color: #666;
            font-size: 0.9em;
            margin-top: 5px;
        }}
        .chart-container {{
            background-color: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
            max-height: 600px;
        }}
        .chart-wrapper {{
            position: relative;
            height: 500px;
        }}
        table.dataTable {{
            width: 100% !important;
            margin-top: 20px !important;
        }}
        table.dataTable thead th {{
            background-color: #4285f4;
            color: white;
            font-weight: bold;
            padding: 12px;
        }}
        table.dataTable tbody td {{
            padding: 10px;
        }}
        table.dataTable tbody tr:hover {{
            background-color: #f5f5f5;
        }}
        .cost-high {{
            color: #d32f2f;
            font-weight: bold;
        }}
        .cost-medium {{
            color: #f57c00;
        }}
        .cost-low {{
            color: #388e3c;
        }}
        .footer {{
            margin-top: 30px;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Terra Workspace Storage Cost Report</h1>
        
        <div class="summary">
            <div class="summary-item">
                <div class="summary-value">{total_workspaces}</div>
                <div class="summary-label">Total Workspaces</div>
            </div>
            <div class="summary-item">
                <div class="summary-value">${total_cost:.2f}</div>
                <div class="summary-label">Total Monthly Cost</div>
            </div>
            <div class="summary-item">
                <div class="summary-value">${avg_cost:.2f}</div>
                <div class="summary-label">Average Cost</div>
            </div>
            <div class="summary-item">
                <div class="summary-value">{nonzero_workspaces}</div>
                <div class="summary-label">Workspaces with Storage</div>
            </div>
        </div>

        <h2>Storage Costs by Workspace</h2>
        <div class="chart-container">
            <div class="chart-wrapper">
                <canvas id="costChart"></canvas>
            </div>
        </div>

        <h2>Detailed Workspace List</h2>
        <table id="storageTable" class="display">
            <thead>
                <tr>
                    <th>Namespace</th>
                    <th>Workspace Name</th>
                    <th>Monthly Cost (USD)</th>
                </tr>
            </thead>
            <tbody>
{table_rows}
            </tbody>
        </table>

        <div class="footer">
            Generated on {timestamp}<br>
            Report created by Altocumulus
        </div>
    </div>

    <script>
        // Chart data
        const workspaceData = {chart_data};

        // Create bar chart
        const ctx = document.getElementById('costChart').getContext('2d');
        const costChart = new Chart(ctx, {{
            type: 'bar',
            data: {{
                labels: workspaceData.map(w => w.namespace + '/' + w.name),
                datasets: [{{
                    label: 'Monthly Cost (USD)',
                    data: workspaceData.map(w => w.cost),
                    backgroundColor: workspaceData.map(w => {{
                        if (w.cost > 10) return 'rgba(211, 47, 47, 0.7)';  // red
                        if (w.cost > 1) return 'rgba(245, 124, 0, 0.7)';   // orange
                        if (w.cost > 0) return 'rgba(56, 142, 60, 0.7)';   // green
                        return 'rgba(158, 158, 158, 0.7)';                  // gray
                    }}),
                    borderColor: workspaceData.map(w => {{
                        if (w.cost > 10) return 'rgba(211, 47, 47, 1)';
                        if (w.cost > 1) return 'rgba(245, 124, 0, 1)';
                        if (w.cost > 0) return 'rgba(56, 142, 60, 1)';
                        return 'rgba(158, 158, 158, 1)';
                    }}),
                    borderWidth: 1
                }}]
            }},
            options: {{
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y',  // Horizontal bar chart
                plugins: {{
                    legend: {{
                        display: false
                    }},
                    tooltip: {{
                        callbacks: {{
                            label: function(context) {{
                                return '$' + context.parsed.x.toFixed(2) + ' / month';
                            }}
                        }}
                    }}
                }},
                scales: {{
                    x: {{
                        beginAtZero: true,
                        title: {{
                            display: true,
                            text: 'Monthly Cost (USD)'
                        }},
                        ticks: {{
                            callback: function(value) {{
                                return '$' + value;
                            }}
                        }}
                    }},
                    y: {{
                        ticks: {{
                            autoSkip: false,
                            font: {{
                                size: 10
                            }}
                        }}
                    }}
                }}
            }}
        }});

        // DataTable
        $(document).ready(function() {{
            $('#storageTable').DataTable({{
                order: [[2, 'desc']],
                pageLength: 25,
                lengthMenu: [[10, 25, 50, 100, -1], [10, 25, 50, 100, "All"]],
                columnDefs: [
                    {{
                        targets: 2,
                        render: function(data, type, row) {{
                            if (type === 'display') {{
                                var cost = parseFloat(data);
                                var cssClass = '';
                                if (cost > 10) cssClass = 'cost-high';
                                else if (cost > 1) cssClass = 'cost-medium';
                                else if (cost > 0) cssClass = 'cost-low';
                                return '<span class="' + cssClass + '">$' + cost.toFixed(2) + '</span>';
                            }}
                            return data;
                        }}
                    }}
                ]
            }});
        }});
    </script>
</body>
</html>
"""


def main(argv):
    parser = argparse.ArgumentParser(
        description="Export workspace storage cost estimates associated with the user"
    )
    parser.add_argument("--output", help="Output TSV path")
    parser.add_argument("--html-output", help="Output HTML report path")
    parser.add_argument(
        "--access",
        help="Workspace access levels",
        choices=["owner", "reader", "writer"],
        action="append",
    )
    args = parser.parse_args(argv)

    if not args.output and not args.html_output:
        parser.error("At least one of --output or --html-output must be specified")

    workspaces = fapi.list_workspaces().json()

    access = args.access
    if access is None:
        access = []
    access_filter = set()
    if "reader" in access:
        access_filter.add("READER")
    if "writer" in access:
        access_filter.add("WRITER")
    if "owner" in access or len(access) == 0:
        access_filter.add("OWNER")

    # Collect all workspace data
    workspace_data = []
    for w in workspaces:
        if w["accessLevel"] in access_filter:
            namespace = w["workspace"]["namespace"]
            name = w["workspace"]["name"]

            # Use the updated API method
            r = fapi.get_storage_cost(namespace, name)
            if r.status_code == 200:
                estimate = r.json()["estimate"]
                workspace_data.append({
                    "namespace": namespace,
                    "name": name,
                    "estimate": estimate
                })
            else:
                print(f"Warning: Could not get storage cost for {namespace}/{name}: {r.status_code}")

    # Sort by cost descending for chart
    workspace_data_sorted = sorted(workspace_data, key=lambda x: x["estimate"], reverse=True)

    # Write TSV output if requested
    if args.output:
        with open(args.output, "wt") as out:
            out.write("namespace\tname\testimate\n")
            for ws in workspace_data:
                out.write(f"{ws['namespace']}\t{ws['name']}\t{ws['estimate']}\n")
        print(f"TSV report written to: {args.output}")

    # Write HTML output if requested
    if args.html_output:
        # Calculate summary statistics
        total_workspaces = len(workspace_data)
        total_cost = sum(ws["estimate"] for ws in workspace_data)
        avg_cost = total_cost / total_workspaces if total_workspaces > 0 else 0
        nonzero_workspaces = sum(1 for ws in workspace_data if ws["estimate"] > 0)

        # Generate table rows
        table_rows = []
        for ws in workspace_data:
            row = f"""                <tr>
                    <td>{ws['namespace']}</td>
                    <td>{ws['name']}</td>
                    <td>{ws['estimate']}</td>
                </tr>"""
            table_rows.append(row)

        # Prepare chart data (limit to top 50 workspaces to keep chart readable)
        chart_data_limited = workspace_data_sorted[:50]
        import json
        chart_data_json = json.dumps([
            {"namespace": ws["namespace"], "name": ws["name"], "cost": ws["estimate"]}
            for ws in chart_data_limited
        ])

        # Generate HTML
        html_content = HTML_TEMPLATE.format(
            total_workspaces=total_workspaces,
            total_cost=total_cost,
            avg_cost=avg_cost,
            nonzero_workspaces=nonzero_workspaces,
            table_rows='\n'.join(table_rows),
            chart_data=chart_data_json,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        with open(args.html_output, "w") as f:
            f.write(html_content)
        print(f"HTML report written to: {args.html_output}")

    print(f"\nSummary: {total_workspaces} workspaces, ${total_cost:.2f} total monthly cost")
