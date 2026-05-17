import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# Initialize Dash App with a Slate/Dark Bootstrap theme
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    suppress_callback_exceptions=True,
    title="Robotaxi Finance Analytics Dashboard"
)

server = app.server

# Load cleaned data
cleaned_dir = r"c:\Users\hpvic\OneDrive\Documents\Finance of Robotaxi\cleaned_data"
trips = pd.read_csv(os.path.join(cleaned_dir, 'ds1_trips_cleaned.csv'))
vehicles = pd.read_csv(os.path.join(cleaned_dir, 'ds1_vehicles_cleaned.csv'))
customers = pd.read_csv(os.path.join(cleaned_dir, 'ds2_customers_cleaned.csv'))
transactions = pd.read_csv(os.path.join(cleaned_dir, 'ds2_transactions_cleaned.csv'))
fleet_vehicles = pd.read_csv(os.path.join(cleaned_dir, 'ds3_fleet_vehicles_cleaned.csv'))
maintenance = pd.read_csv(os.path.join(cleaned_dir, 'ds3_maintenance_records_cleaned.csv'))
incidents = pd.read_csv(os.path.join(cleaned_dir, 'ds4_incidents_cleaned.csv'))
insurance = pd.read_csv(os.path.join(cleaned_dir, 'ds4_insurance_policies_cleaned.csv'))

# Pre-calculate main values
net_trip_revenue = trips['fare_amount_usd'].sum() - trips['discount_applied_usd'].sum()
total_maint_cost = maintenance['total_cost_usd'].sum()
driver_payout = transactions['driver_payout_usd'].sum()
annual_insurance_premium = insurance['premium_monthly_usd'].sum() * 12
total_claims = incidents['settlement_amount_usd'].sum()
actual_loss_ratio = (total_claims / annual_insurance_premium) * 100

# Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    
    # Sidebar Panel
    html.Div([
        html.Div([
            html.Span("🚕 ", style={'fontSize': '2rem', 'verticalAlign': 'middle'}),
            html.Span("ROBOTAXI OPS", style={
                'fontSize': '1.35rem', 
                'fontWeight': '800', 
                'verticalAlign': 'middle',
                'background': 'linear-gradient(135deg, #ffffff 0%, #cbd5e1 100%)',
                '-webkit-background-clip': 'text',
                '-webkit-text-fill-color': 'transparent'
            })
        ], style={'marginBottom': '30px', 'textAlign': 'center'}),
        
        html.Hr(style={'borderColor': '#1e293b'}),
        
        html.Div([
            html.Button("📈 Executive Overview", id="btn-overview", className="menu-btn menu-btn-active"),
            html.Button("🗺️ Perjalanan & Rute", id="btn-trips", className="menu-btn"),
            html.Button("💳 Finansial & Transaksi", id="btn-financials", className="menu-btn"),
            html.Button("👥 Perilaku Pelanggan", id="btn-customers", className="menu-btn"),
            html.Button("🔧 Pemeliharaan Armada", id="btn-maintenance", className="menu-btn"),
            html.Button("💥 Manajemen Asuransi", id="btn-insurance", className="menu-btn"),
        ], id="sidebar-menu", style={'marginTop': '25px'}),
        
        html.Div([
            st_info_card := html.Div([
                html.Small("📊 PRO TIP FOR PORTFOLIO", style={'fontWeight': 'bold', 'color': '#60a5fa', 'fontSize': '10px'}),
                html.P("Gunakan temuan asuransi (Loss Ratio 22.29%) untuk bernegosiasi premi tahunan di modul Asuransi!", 
                       style={'margin': '5px 0 0 0', 'fontSize': '11px', 'color': '#94a3b8', 'lineHeight': '1.4'})
            ], style={
                'background': 'rgba(30, 41, 59, 0.4)', 
                'border': '1px solid #1e293b', 
                'borderRadius': '8px', 
                'padding': '12px',
                'marginTop': '60px'
            })
        ])
    ], className="sidebar-panel"),
    
    # Main Content Area
    html.Div(id="main-content", className="content-panel")
])

# Callback for Active Menu buttons styling and Content Routing
@app.callback(
    [
        Output("main-content", "children"),
        Output("btn-overview", "className"),
        Output("btn-trips", "className"),
        Output("btn-financials", "className"),
        Output("btn-customers", "className"),
        Output("btn-maintenance", "className"),
        Output("btn-insurance", "className"),
    ],
    [
        Input("btn-overview", "n_clicks"),
        Input("btn-trips", "n_clicks"),
        Input("btn-financials", "n_clicks"),
        Input("btn-customers", "n_clicks"),
        Input("btn-maintenance", "n_clicks"),
        Input("btn-insurance", "n_clicks"),
    ]
)
def route_tabs(*args):
    ctx = dash.callback_context
    button_id = "btn-overview"
    if ctx.triggered:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        
    # Styles for buttons
    btn_styles = ["menu-btn"] * 6
    btn_list = ["btn-overview", "btn-trips", "btn-financials", "btn-customers", "btn-maintenance", "btn-insurance"]
    active_idx = btn_list.index(button_id)
    btn_styles[active_idx] = "menu-btn menu-btn-active"
    
    # Page Content Selection
    if button_id == "btn-trips":
        content = render_trips_page()
    elif button_id == "btn-financials":
        content = render_financials_page()
    elif button_id == "btn-customers":
        content = render_customers_page()
    elif button_id == "btn-maintenance":
        content = render_maintenance_page()
    elif button_id == "btn-insurance":
        content = render_insurance_page()
    else:
        content = render_overview_page()
        
    return [content] + btn_styles


# ================== PAGE 1: OVERVIEW PAGE RENDER ==================
def render_overview_page():
    # Fig: Profit Comparison
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        name='Pendapatan Bersih',
        x=['Tiket Perjalanan', 'Net Revenue Transaksi'],
        y=[net_trip_revenue, transactions['net_revenue_usd'].sum()],
        marker=dict(color='#60a5fa', line=dict(color='rgba(0,0,0,0)')),
        width=0.4
    ))
    fig_bar.add_trace(go.Bar(
        name='Pengeluaran Bersih',
        x=['Pemeliharaan Armada', 'Safety Driver Payout'],
        y=[total_maint_cost, driver_payout],
        marker=dict(color='#f87171', line=dict(color='rgba(0,0,0,0)')),
        width=0.4
    ))
    fig_bar.update_layout(
        barmode='group',
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        margin=dict(l=20, r=20, t=10, b=20),
        xaxis=dict(gridcolor='#1e293b'),
        yaxis=dict(gridcolor='#1e293b')
    )
    
    return html.Div([
        html.H1("📈 Executive Overview Dashboard", className="glow-header"),
        html.P("Ringkasan Kesehatan Finansial dan Operasional Armada Robotaxi.", style={'color': '#64748b', 'marginBottom': '30px'}),
        
        # Row 1: KPI Cards
        dbc.Row([
            dbc.Col(html.Div([
                html.Small("PENDAPATAN BERSIH PERJALANAN", style={'color': '#94a3b8', 'fontWeight': 'bold', 'fontSize': '11px'}),
                html.Div(f"${net_trip_revenue:,.2f}", className="metric-value", style={'color': '#60a5fa'})
            ], className="glass-card"), width=3),
            dbc.Col(html.Div([
                html.Small("BIAYA PEMELIHARAAN BENGKEL", style={'color': '#94a3b8', 'fontWeight': 'bold', 'fontSize': '11px'}),
                html.Div(f"${total_maint_cost:,.2f}", className="metric-value", style={'color': '#f87171'})
            ], className="glass-card"), width=3),
            dbc.Col(html.Div([
                html.Small("SAFETY DRIVER PAYOUT", style={'color': '#94a3b8', 'fontWeight': 'bold', 'fontSize': '11px'}),
                html.Div(f"${driver_payout:,.2f}", className="metric-value", style={'color': '#fb923c'})
            ], className="glass-card"), width=3),
            dbc.Col(html.Div([
                html.Small("LOSS RATIO ASURANSI", style={'color': '#94a3b8', 'fontWeight': 'bold', 'fontSize': '11px'}),
                html.Div(f"{actual_loss_ratio:.2f}%", className="metric-value", style={'color': '#34d399'})
            ], className="glass-card"), width=3),
        ]),
        
        # Row 2: Alerts
        dbc.Row([
            dbc.Col(html.Div([
                html.H5("🔧 Krisis Defisit Perawatan Bengkel", style={'color': '#f87171', 'fontWeight': 'bold'}),
                html.P(f"Pengeluaran bengkel kita mencapai ${total_maint_cost:,.2f}, atau setara dengan {total_maint_cost/net_trip_revenue:.2f}x pendapatan tiket taksi! Vendor bengkel berindikasi mematok tarif seragam ($260 s/d $300) untuk seluruh layanan, yang menimbulkan kerugian sangat parah.", 
                       style={'margin': '0', 'fontSize': '14px', 'lineHeight': '1.5'})
            ], className="leak-badge"), width=6),
            
            dbc.Col(html.Div([
                html.H5("🛡️ Potensi Penghematan Premi Asuransi", style={'color': '#34d399', 'fontWeight': 'bold'}),
                html.P(f"Dengan Loss Ratio sangat rendah ({actual_loss_ratio:.2f}%), armada otonom kita terbukti sangat aman di jalan raya. Kita dapat menegosiasikan premi turun 40-50%, berpotensi menghemat kas hingga ${(annual_insurance_premium*0.4)/1000000:.2f} Juta per tahun!", 
                       style={'margin': '0', 'fontSize': '14px', 'lineHeight': '1.5'})
            ], className="safe-badge"), width=6),
        ], style={'marginBottom': '20px'}),
        
        # Row 3: Main Chart
        html.Div([
            html.H4("Pendapatan Bersih vs Pengeluaran Bocor Perusahaan", style={'marginBottom': '15px', 'fontWeight': 'bold'}),
            dcc.Graph(figure=fig_bar)
        ], className="glass-card")
    ])


# ================== PAGE 2: TRIPS PAGE RENDER ==================
def render_trips_page():
    # Pie: Trips Status
    status_df = trips['trip_status'].value_counts().reset_index()
    status_df.columns = ['Status', 'Jumlah']
    fig_pie = px.pie(
        status_df, 
        values='Jumlah', 
        names='Status', 
        hole=0.45,
        color_discrete_sequence=px.colors.sequential.Plotly3
    )
    fig_pie.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        margin=dict(l=10, r=10, t=10, b=10)
    )
    
    # Scatter: Distance vs Fare
    sample_trips = trips.sample(n=1000, random_state=42)
    fig_scatter = px.scatter(
        sample_trips, 
        x="distance_km", 
        y="fare_amount_usd", 
        color="route_type",
        hover_data=["trip_duration_mins", "weather_condition"],
        color_discrete_sequence=px.colors.qualitative.Safe
    )
    fig_scatter.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        margin=dict(l=10, r=10, t=30, b=10)
    )
    
    return html.Div([
        html.H1("🗺️ Analisis Perjalanan & Kinerja Rute", className="glow-header"),
        html.P("Analisis sebaran rute, status penyelesaian perjalanan, dan korelasi tarif.", style={'color': '#64748b', 'marginBottom': '30px'}),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5("Sebaran Status Perjalanan", style={'fontWeight': 'bold', 'marginBottom': '15px'}),
                    dcc.Graph(figure=fig_pie)
                ], className="glass-card")
            ], width=4),
            
            dbc.Col([
                html.Div([
                    html.H5("Hubungan Jarak vs Tarif Perjalanan (Sampel 1.000)", style={'fontWeight': 'bold', 'marginBottom': '15px'}),
                    dcc.Graph(figure=fig_scatter)
                ], className="glass-card")
            ], width=8)
        ])
    ])


# ================== PAGE 3: FINANCIALS PAGE RENDER ==================
def render_financials_page():
    # Pie: Transaction Allocation
    fig_pie_tx = go.Figure(data=[go.Pie(
        labels=['Driver Payout', 'Net Revenue', 'Taxes & Other Fees'],
        values=[driver_payout, transactions['net_revenue_usd'].sum(), transactions['gross_amount_usd'].sum() - driver_payout - transactions['net_revenue_usd'].sum()],
        hole=0.5,
        marker=dict(colors=['#f87171', '#60a5fa', '#34d399'])
    )])
    fig_pie_tx.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        margin=dict(l=10, r=10, t=10, b=10)
    )
    
    # Line: GTV Trend
    daily_tx = transactions.groupby('transaction_date')['gross_amount_usd'].sum().reset_index()
    fig_line_tx = px.line(daily_tx, x='transaction_date', y='gross_amount_usd', color_discrete_sequence=['#60a5fa'])
    fig_line_tx.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        margin=dict(l=10, r=10, t=30, b=10)
    )
    
    return html.Div([
        html.H1("💳 Finansial & Aliran Transaksi", className="glow-header"),
        html.P("Pelacakan transaksi kotor, pembayaran safety driver, dan margin pendapatan.", style={'color': '#64748b', 'marginBottom': '30px'}),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5("Alokasi Transaksi Kotor (GTV)", style={'fontWeight': 'bold', 'marginBottom': '15px'}),
                    dcc.Graph(figure=fig_pie_tx)
                ], className="glass-card")
            ], width=4),
            
            dbc.Col([
                html.Div([
                    html.H5("Tren Harian Gross Transaction Value (GTV)", style={'fontWeight': 'bold', 'marginBottom': '15px'}),
                    dcc.Graph(figure=fig_line_tx)
                ], className="glass-card")
            ], width=8)
        ])
    ])


# ================== PAGE 4: CUSTOMERS PAGE RENDER ==================
def render_customers_page():
    loyalty_df = customers.groupby('loyalty_tier').agg(
        total_users=('customer_id', 'count'),
        avg_spent=('total_spent_usd', 'mean'),
        avg_churn_risk=('churn_risk_score', 'mean')
    ).reset_index()
    
    # Chart: Total Users
    fig_c1 = px.bar(loyalty_df, x='loyalty_tier', y='total_users', color='loyalty_tier', color_discrete_sequence=px.colors.sequential.Agsunset)
    fig_c1.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=10, b=10))
    
    # Chart: Avg Churn
    fig_c2 = px.line(loyalty_df, x='loyalty_tier', y='avg_churn_risk', markers=True, color_discrete_sequence=['#ff007f'])
    fig_c2.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=10, b=10))
    
    return html.Div([
        html.H1("👥 Perilaku Pelanggan & Risiko Churn", className="glow-header"),
        html.P("Analisis sebaran loyalis pelanggan, kontribusi pengeluaran, dan prediksi risiko retensi.", style={'color': '#64748b', 'marginBottom': '30px'}),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5("Sebaran Jumlah Pelanggan Per Loyalty Tier", style={'fontWeight': 'bold', 'marginBottom': '15px'}),
                    dcc.Graph(figure=fig_c1)
                ], className="glass-card")
            ], width=6),
            
            dbc.Col([
                html.Div([
                    html.H5("Tingkat Risiko Churn Rata-rata Pelanggan", style={'fontWeight': 'bold', 'marginBottom': '15px'}),
                    dcc.Graph(figure=fig_c2)
                ], className="glass-card")
            ], width=6)
        ])
    ])


# ================== PAGE 5: MAINTENANCE PAGE RENDER ==================
def render_maintenance_page():
    maint_summary = maintenance.groupby('service_type').agg(
        total_cost=('total_cost_usd', 'sum'),
        avg_downtime=('downtime_hours', 'mean')
    ).reset_index().sort_values(by='total_cost', ascending=False)
    
    fig_ms1 = px.bar(maint_summary, x='total_cost', y='service_type', orientation='h', color='service_type', color_discrete_sequence=px.colors.sequential.Magma)
    fig_ms1.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=10, b=10))
    
    return html.Div([
        html.H1("🔧 Biaya Pemeliharaan Armada (Maintenance)", className="glow-header"),
        html.P("Analisis pembengkakan biaya pemeliharaan berkala, jenis perawatan termahal, dan downtime.", style={'color': '#64748b', 'marginBottom': '30px'}),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5("Total Pengeluaran Bengkel Berdasarkan Jenis Layanan", style={'fontWeight': 'bold', 'marginBottom': '15px'}),
                    dcc.Graph(figure=fig_ms1)
                ], className="glass-card")
            ], width=12)
        ])
    ])


# ================== PAGE 6: INSURANCE PAGE RENDER (SIMULATOR) ==================
def render_insurance_page():
    inc_summary = incidents.groupby('incident_type')['settlement_amount_usd'].agg(['sum', 'count']).reset_index().sort_values(by='sum', ascending=False)
    
    fig_inc1 = px.bar(inc_summary, x='incident_type', y='sum', color='incident_type', color_discrete_sequence=px.colors.sequential.Viridis)
    fig_inc1.update_layout(template='plotly_dark', paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=10, r=10, t=10, b=10))
    
    return html.Div([
        html.H1("🛡️ Manajemen Risiko & Simulator Premi Asuransi", className="glow-header"),
        html.P("Simulator interaktif bagi CFO untuk merancang strategi penghematan premi tahunan berdasarkan tingkat keamanan.", style={'color': '#64748b', 'marginBottom': '30px'}),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H4("🎛️ Simulator Negosiasi Premi Asuransi", style={'fontWeight': 'bold', 'color': '#60a5fa', 'marginBottom': '15px'}),
                    html.P("Tingkat kecelakaan kita yang sangat rendah (Loss Ratio 22.29%) memberi kita leverage negosiasi. Geser slider untuk menyimulasikan persentase diskon premi tahunan yang bisa kita hemat:", style={'fontSize': '14px', 'color': '#94a3b8'}),
                    
                    html.Div([
                        dcc.Slider(
                            id='insurance-slider',
                            min=0,
                            max=60,
                            step=5,
                            value=30,
                            marks={i: f'{i}%' for i in range(0, 61, 10)},
                            className="custom-slider"
                        )
                    ], style={'padding': '20px 10px 40px 10px'}),
                    
                    dbc.Row([
                        dbc.Col(html.Div([
                            html.Small("KAS YANG DIHEMAT PER TAHUN", style={'color': '#94a3b8', 'fontSize': '11px', 'fontWeight': 'bold'}),
                            html.Div(id='saved-premium-box', className="metric-value", style={'color': '#34d399', 'fontSize': '1.75rem'})
                        ], style={'background': 'rgba(52, 211, 153, 0.05)', 'border': '1px solid rgba(52, 211, 153, 0.15)', 'padding': '15px', 'borderRadius': '10px'}), width=6),
                        
                        dbc.Col(html.Div([
                            html.Small("ESTIMASI PREMI TAHUNAN BARU", style={'color': '#94a3b8', 'fontSize': '11px', 'fontWeight': 'bold'}),
                            html.Div(id='new-premium-box', className="metric-value", style={'color': '#60a5fa', 'fontSize': '1.75rem'})
                        ], style={'background': 'rgba(96, 165, 250, 0.05)', 'border': '1px solid rgba(96, 165, 250, 0.15)', 'padding': '15px', 'borderRadius': '10px'}), width=6),
                    ])
                ], className="glass-card")
            ], width=12),
        ]),
        
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5("Total Penyelesaian Klaim Asuransi Berdasarkan Jenis Insiden", style={'fontWeight': 'bold', 'marginBottom': '15px'}),
                    dcc.Graph(figure=fig_inc1)
                ], className="glass-card")
            ], width=12)
        ])
    ])


# Callback for Insurance Negotiation Simulator
@app.callback(
    [
        Output('saved-premium-box', 'children'),
        Output('new-premium-box', 'children')
    ],
    [Input('insurance-slider', 'value')]
)
def update_simulator(discount_pct):
    saved_amount = annual_insurance_premium * (discount_pct / 100.0)
    new_premium = annual_insurance_premium - saved_amount
    return f"${saved_amount:,.2f}", f"${new_premium:,.2f}"


if __name__ == '__main__':
    # Running Dash locally
    app.run(debug=True, port=8050)
