import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title="European Heatwave Crisis 2026",
    page_icon="🌡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border: 1px solid #e74c3c;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(231,76,60,0.2);
    }
    .metric-value { font-size: 2.5rem; font-weight: bold; color: #e74c3c; }
    .metric-label { font-size: 0.9rem; color: #aaa; margin-top: 5px; }
    .insight-box {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-left: 4px solid #e74c3c;
        border-radius: 8px;
        padding: 15px;
        margin: 8px 0;
        color: #eee;
        font-size: 0.9rem;
    }
    .predict-box {
        background: linear-gradient(135deg, #1a1a2e, #16213e);
        border-left: 4px solid #f39c12;
        border-radius: 8px;
        padding: 15px;
        margin: 8px 0;
        color: #eee;
        font-size: 0.9rem;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    temp     = pd.read_csv("data/temperature_data.csv")
    health   = pd.read_csv("data/health_impact.csv")
    monthly  = pd.read_csv("data/monthly_trends.csv")
    response = pd.read_csv("data/response_data.csv")
    forecast = pd.read_csv("data/forecast_jul_aug.csv")
    return temp, health, monthly, response, forecast

temp_df, health_df, monthly_df, response_df, forecast_df = load_data()
merged = temp_df.merge(health_df, on="country").merge(response_df, on="country")

# ── SIDEBAR ──────────────────────────────────────────────────────
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Flag_of_Europe.svg/320px-Flag_of_Europe.svg.png", width=120)
    st.title("🌡️ Heatwave 2026")
    st.markdown("---")
    selected_countries = st.multiselect(
        "Filter Countries",
        options=temp_df["country"].tolist(),
        default=temp_df["country"].tolist()
    )
    crisis_filter = st.multiselect(
        "Crisis Level",
        options=["Extreme","Severe","Moderate","Low"],
        default=["Extreme","Severe","Moderate","Low"]
    )
    st.markdown("---")
    st.markdown("**Data Sources**")
    st.markdown("🌍 Open-Meteo API (Live)")
    st.markdown("🏥 ECDC Health Data 2023")
    st.markdown("🌐 WHO Europe Reports")
    st.markdown("🤖 ML Trend Forecasting")

filtered = merged[
    (merged["country"].isin(selected_countries)) &
    (merged["crisis_level"].isin(crisis_filter))
]
forecast_filtered = forecast_df[forecast_df["country"].isin(selected_countries)]

color_map = {"Extreme":"#e74c3c","Severe":"#e67e22","Moderate":"#f1c40f","Low":"#2ecc71"}

tab1, tab2, tab3, tab4 = st.tabs([
    "🌡️ Heatwave Severity",
    "🔮 July–Aug Forecast",
    "🏥 Human Impact",
    "🛡️ Response & Support"
])

# ════════════════════════════════════════════════════════════════
# TAB 1 — HEATWAVE SEVERITY
# ════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("## 🌡️ European Heatwave Crisis 2026 — Severity Overview")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">{filtered['peak_temp_2026'].max():.1f}°C</div>
            <div class="metric-label">🔥 Peak Temperature Recorded</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        extreme = len(filtered[filtered["crisis_level"]=="Extreme"])
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">{extreme}</div>
            <div class="metric-label">🚨 Countries in Extreme Crisis</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">{filtered['days_above_35c'].max()}</div>
            <div class="metric-label">📅 Max Days Above 35°C</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">{filtered['temp_anomaly'].mean():.1f}°C</div>
            <div class="metric-label">📈 Avg Temperature Anomaly</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        fig_map = px.choropleth(
            filtered, locations="country_code", color="peak_temp_2026",
            hover_name="country",
            hover_data={"peak_temp_2026":True,"crisis_level":True,"days_above_35c":True},
            color_continuous_scale=["#fff7bc","#feb24c","#f03b20","#bd0026"],
            range_color=[25,50], scope="europe",
            title="🗺️ Peak Temperature by Country (Jan–Jun 2026)",
            labels={"peak_temp_2026":"Peak Temp (°C)"}
        )
        fig_map.update_layout(
            paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font_color="white",
            geo=dict(bgcolor="#0e1117", lakecolor="#0e1117", landcolor="#1a1a2e",
                     showcoastlines=True, coastlinecolor="#444")
        )
        st.plotly_chart(fig_map, use_container_width=True)

    with col2:
        sorted_df = filtered.sort_values("peak_temp_2026", ascending=True)
        colors = [color_map.get(c,"#888") for c in sorted_df["crisis_level"]]
        fig_bar = go.Figure(go.Bar(
            x=sorted_df["peak_temp_2026"], y=sorted_df["country"],
            orientation="h", marker_color=colors,
            text=sorted_df["peak_temp_2026"].apply(lambda x: f"{x}°C"),
            textposition="outside"
        ))
        fig_bar.update_layout(
            title="🌡️ Peak Temperature Ranking",
            paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font_color="white",
            xaxis=dict(title="Temperature (°C)", gridcolor="#333"),
            yaxis=dict(gridcolor="#333"), height=400
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        monthly_filtered = monthly_df[
            (monthly_df["country"].isin(selected_countries[:6])) &
            (monthly_df["type"] == "Actual")
        ]
        fig_trend = px.line(
            monthly_filtered, x="month", y="avg_temp", color="country",
            title="📈 Monthly Temperature Trend (Actual Jan–Jun 2026)", markers=True
        )
        fig_trend.update_layout(
            paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font_color="white",
            xaxis=dict(gridcolor="#333"), yaxis=dict(gridcolor="#333", title="Avg Temp (°C)"),
            legend=dict(bgcolor="#1a1a2e")
        )
        st.plotly_chart(fig_trend, use_container_width=True)

    with col4:
        anom_sorted = filtered.sort_values("temp_anomaly", ascending=False)
        fig_anom = px.bar(
            anom_sorted, x="country", y="temp_anomaly",
            color="temp_anomaly",
            color_continuous_scale=["#fee08b","#f46d43","#d73027","#a50026"],
            title="⚠️ Temperature Anomaly vs Historical Average",
            text="temp_anomaly"
        )
        fig_anom.update_traces(texttemplate="%{text}°C", textposition="outside")
        fig_anom.update_layout(
            paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font_color="white",
            xaxis=dict(gridcolor="#333", tickangle=-30),
            yaxis=dict(gridcolor="#333", title="Anomaly (°C)"),
            coloraxis_showscale=False, height=380
        )
        st.plotly_chart(fig_anom, use_container_width=True)

# ════════════════════════════════════════════════════════════════
# TAB 2 — FORECAST
# ════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("## 🔮 ML Forecast — Predicted Temperatures July–August 2026")
    st.info("📊 Predictions based on linear trend analysis of 2015–2025 historical data from Open-Meteo API")

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">{forecast_filtered['predicted_peak_jul_aug'].max():.1f}°C</div>
            <div class="metric-label">🔮 Predicted Peak Temp</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        hottest = forecast_filtered.loc[forecast_filtered['predicted_peak_jul_aug'].idxmax(),'country']
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">{hottest}</div>
            <div class="metric-label">🌍 Hottest Country Predicted</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        avg_pred = forecast_filtered['predicted_peak_jul_aug'].mean()
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">{avg_pred:.1f}°C</div>
            <div class="metric-label">📊 Avg Predicted Peak</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        avg_anom = forecast_filtered['predicted_anomaly'].mean()
        st.markdown(f"""<div class="metric-card">
            <div class="metric-value">+{avg_anom:.1f}°C</div>
            <div class="metric-label">⚠️ Avg Predicted Anomaly</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)

    with col1:
        # Forecast bar with confidence intervals
        fc_sorted = forecast_filtered.sort_values("predicted_peak_jul_aug", ascending=True)
        fig_fc = go.Figure()
        fig_fc.add_trace(go.Bar(
            x=fc_sorted["predicted_peak_jul_aug"],
            y=fc_sorted["country"],
            orientation="h",
            marker_color="#f39c12",
            name="Predicted Peak",
            text=fc_sorted["predicted_peak_jul_aug"].apply(lambda x: f"{x}°C"),
            textposition="outside",
            error_x=dict(
                type="data",
                symmetric=False,
                array=fc_sorted["confidence_upper"] - fc_sorted["predicted_peak_jul_aug"],
                arrayminus=fc_sorted["predicted_peak_jul_aug"] - fc_sorted["confidence_lower"],
                color="#e74c3c"
            )
        ))
        fig_fc.update_layout(
            title="🔮 Predicted Peak Temp Jul–Aug 2026 (with confidence range)",
            paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font_color="white",
            xaxis=dict(title="Temperature (°C)", gridcolor="#333", range=[25, 55]),
            yaxis=dict(gridcolor="#333"), height=420
        )
        st.plotly_chart(fig_fc, use_container_width=True)

    with col2:
        # Full year trend (actual + predicted)
        monthly_top6 = monthly_df[monthly_df["country"].isin(selected_countries[:6])]
        fig_full = go.Figure()
        top6 = selected_countries[:6]
        colors_line = ["#e74c3c","#3498db","#2ecc71","#f39c12","#9b59b6","#1abc9c"]
        for i, country in enumerate(top6):
            actual = monthly_top6[(monthly_top6["country"]==country) & (monthly_top6["type"]=="Actual")]
            predicted = monthly_top6[(monthly_top6["country"]==country) & (monthly_top6["type"]=="Predicted")]
            c = colors_line[i % len(colors_line)]
            fig_full.add_trace(go.Scatter(
                x=actual["month"], y=actual["avg_temp"],
                mode="lines+markers", name=f"{country} (Actual)",
                line=dict(color=c, width=2), marker=dict(size=6)
            ))
            if not predicted.empty:
                fig_full.add_trace(go.Scatter(
                    x=predicted["month"], y=predicted["avg_temp"],
                    mode="markers", name=f"{country} (Predicted)",
                    marker=dict(symbol="star", size=12, color=c),
                    showlegend=False
                ))
        fig_full.update_layout(
            title="📈 Full Year Trend: Actual (Jan–Jun) + Predicted (Jul–Aug)",
            paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font_color="white",
            xaxis=dict(gridcolor="#333", categoryorder="array",
                       categoryarray=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug"]),
            yaxis=dict(gridcolor="#333", title="Avg Temp (°C)"),
            legend=dict(bgcolor="#1a1a2e")
        )
        st.plotly_chart(fig_full, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        # Predicted anomaly
        fig_pred_anom = px.bar(
            forecast_filtered.sort_values("predicted_anomaly", ascending=False),
            x="country", y="predicted_anomaly",
            color="predicted_anomaly",
            color_continuous_scale=["#fdae61","#f46d43","#d73027","#a50026"],
            title="⚠️ Predicted Temperature Anomaly (Jul–Aug vs Historical)",
            text="predicted_anomaly"
        )
        fig_pred_anom.update_traces(texttemplate="+%{text}°C", textposition="outside")
        fig_pred_anom.update_layout(
            paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font_color="white",
            xaxis=dict(gridcolor="#333", tickangle=-30),
            yaxis=dict(gridcolor="#333"), coloraxis_showscale=False
        )
        st.plotly_chart(fig_pred_anom, use_container_width=True)

    with col4:
        # Forecast map
        fig_fmap = px.choropleth(
            forecast_filtered, locations="country_code",
            color="predicted_peak_jul_aug",
            hover_name="country",
            hover_data={"predicted_peak_jul_aug":True,"predicted_anomaly":True},
            color_continuous_scale=["#fff7bc","#feb24c","#f03b20","#bd0026"],
            range_color=[25,55], scope="europe",
            title="🗺️ Predicted Peak Temp Map (Jul–Aug 2026)",
            labels={"predicted_peak_jul_aug":"Predicted Peak (°C)"}
        )
        fig_fmap.update_layout(
            paper_bgcolor="#0e1117", font_color="white",
            geo=dict(bgcolor="#0e1117", lakecolor="#0e1117",
                     landcolor="#1a1a2e", showcoastlines=True, coastlinecolor="#444")
        )
        st.plotly_chart(fig_fmap, use_container_width=True)

    st.markdown("### 🤖 Forecast Methodology")
    st.markdown("""
    <div class="predict-box">
    <b>📐 Model:</b> Linear trend regression trained on 11 years of Open-Meteo historical data (2015–2025)<br><br>
    <b>📊 Input:</b> Daily maximum temperatures for July–August each year per country capital<br><br>
    <b>🎯 Output:</b> Predicted 2026 peak temperature with ±1.5σ confidence interval<br><br>
    <b>⚠️ Note:</b> Predictions will be updated with real data as July–August 2026 progresses
    </div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# TAB 3 — HUMAN IMPACT
# ════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("## 🏥 Human Impact — Deaths, Hospitalisations & Vulnerable Groups")
    c1, c2, c3, c4 = st.columns(4)
    total_deaths = filtered["heat_deaths_2026_est"].sum()
    total_hosp   = filtered["hospital_admissions"].sum()
    total_aff    = filtered["people_affected_M"].sum()
    avg_eld      = filtered["elderly_pop_pct"].mean()

    for col, val, label in zip(
        [c1,c2,c3,c4],
        [f"{total_deaths:,}", f"{total_hosp:,}", f"{total_aff:.1f}M", f"{avg_eld:.1f}%"],
        ["💀 Est. Heat Deaths 2026","🏥 Hospital Admissions","👥 People Affected","👴 Avg Elderly Population"]
    ):
        with col:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        death_data = filtered[["country","heat_deaths_2023","heat_deaths_2026_est"]].melt(
            id_vars="country", var_name="Year", value_name="Deaths"
        )
        death_data["Year"] = death_data["Year"].map({
            "heat_deaths_2023":"2023 (Verified)",
            "heat_deaths_2026_est":"2026 (Estimated)"
        })
        fig_deaths = px.bar(
            death_data, x="country", y="Deaths", color="Year", barmode="group",
            color_discrete_map={"2023 (Verified)":"#3498db","2026 (Estimated)":"#e74c3c"},
            title="💀 Heat-Related Deaths: 2023 vs 2026 Estimate"
        )
        fig_deaths.update_layout(
            paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font_color="white",
            xaxis=dict(gridcolor="#333", tickangle=-30),
            yaxis=dict(gridcolor="#333"), legend=dict(bgcolor="#1a1a2e")
        )
        st.plotly_chart(fig_deaths, use_container_width=True)

    with col2:
        fig_hosp = px.bar(
            filtered.sort_values("hospital_admissions", ascending=False),
            x="country", y="hospital_admissions",
            color="hospital_admissions",
            color_continuous_scale=["#fdae61","#f46d43","#d73027"],
            title="🏥 Hospital Admissions by Country",
            text="hospital_admissions"
        )
        fig_hosp.update_traces(texttemplate="%{text:,}", textposition="outside")
        fig_hosp.update_layout(
            paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font_color="white",
            xaxis=dict(gridcolor="#333", tickangle=-30),
            yaxis=dict(gridcolor="#333"), coloraxis_showscale=False
        )
        st.plotly_chart(fig_hosp, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        fig_bubble = px.scatter(
            filtered, x="peak_temp_2026", y="heat_deaths_2026_est",
            size="people_affected_M", color="crisis_level",
            hover_name="country", text="country",
            color_discrete_map=color_map,
            title="🔴 Deaths vs Peak Temperature (bubble = people affected)",
            size_max=60
        )
        fig_bubble.update_traces(textposition="top center")
        fig_bubble.update_layout(
            paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font_color="white",
            xaxis=dict(gridcolor="#333", title="Peak Temp (°C)"),
            yaxis=dict(gridcolor="#333", title="Est. Deaths 2026"),
            legend=dict(bgcolor="#1a1a2e")
        )
        st.plotly_chart(fig_bubble, use_container_width=True)

    with col4:
        fig_eld = px.scatter(
            filtered, x="elderly_pop_pct", y="heat_deaths_2026_est",
            color="crisis_level", hover_name="country", text="country",
            color_discrete_map=color_map,
            trendline="ols",
            title="👴 Elderly Population % vs Heat Deaths"
        )
        fig_eld.update_traces(textposition="top center")
        fig_eld.update_layout(
            paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font_color="white",
            xaxis=dict(gridcolor="#333", title="Elderly Population (%)"),
            yaxis=dict(gridcolor="#333", title="Est. Deaths 2026"),
            legend=dict(bgcolor="#1a1a2e")
        )
        st.plotly_chart(fig_eld, use_container_width=True)

    st.markdown("### 💡 Key Insights")
    worst = filtered.loc[filtered["heat_deaths_2026_est"].idxmax(),"country"]
    increase = ((filtered["heat_deaths_2026_est"].sum() - filtered["heat_deaths_2023"].sum()) /
                filtered["heat_deaths_2023"].sum() * 100)
    st.markdown(f"""
    <div class="insight-box">🚨 <b>{worst}</b> has the highest estimated heat deaths in 2026.</div>
    <div class="insight-box">📈 Heat deaths across Europe are estimated to increase by <b>{increase:.0f}%</b> vs 2023.</div>
    <div class="insight-box">👴 Countries with elderly populations above 23% face disproportionately higher mortality.</div>
    <div class="insight-box">🏥 Total hospital admissions expected to exceed <b>{total_hosp:,}</b> — straining healthcare systems.</div>
    """, unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════
# TAB 4 — RESPONSE & SUPPORT
# ════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("## 🛡️ Government Response & Support Infrastructure")
    c1, c2, c3, c4 = st.columns(4)
    for col, val, label in zip(
        [c1,c2,c3,c4],
        [f"{filtered['cooling_centres'].sum():,}",
         f"£{filtered['emergency_budget_mn'].sum():,}M",
         f"{filtered['water_stations'].sum():,}",
         f"{filtered['response_score'].mean():.0f}/100"],
        ["❄️ Cooling Centres","💰 Emergency Budget","💧 Water Stations","📊 Avg Response Score"]
    ):
        with col:
            st.markdown(f"""<div class="metric-card">
                <div class="metric-value">{val}</div>
                <div class="metric-label">{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        resp_sorted = filtered.sort_values("response_score", ascending=True)
        colors_resp = ["#e74c3c" if s<60 else "#e67e22" if s<75 else "#2ecc71"
                       for s in resp_sorted["response_score"]]
        fig_resp = go.Figure(go.Bar(
            x=resp_sorted["response_score"], y=resp_sorted["country"],
            orientation="h", marker_color=colors_resp,
            text=resp_sorted["response_score"].apply(lambda x: f"{x}/100"),
            textposition="outside"
        ))
        fig_resp.update_layout(
            title="📊 Government Response Score (0–100)",
            paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font_color="white",
            xaxis=dict(gridcolor="#333", range=[0,110]),
            yaxis=dict(gridcolor="#333"), height=400
        )
        st.plotly_chart(fig_resp, use_container_width=True)

    with col2:
        fig_cc = px.scatter(
            filtered, x="emergency_budget_mn", y="cooling_centres",
            size="response_score", color="crisis_level", text="country",
            color_discrete_map=color_map,
            title="❄️ Cooling Centres vs Emergency Budget", size_max=40
        )
        fig_cc.update_traces(textposition="top center")
        fig_cc.update_layout(
            paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font_color="white",
            xaxis=dict(gridcolor="#333", title="Emergency Budget (£M)"),
            yaxis=dict(gridcolor="#333", title="Cooling Centres"),
            legend=dict(bgcolor="#1a1a2e")
        )
        st.plotly_chart(fig_cc, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        alert_counts = filtered["alert_system"].value_counts().reset_index()
        alert_counts.columns = ["Has Alert System","Count"]
        fig_alert = px.pie(
            alert_counts, names="Has Alert System", values="Count",
            color_discrete_sequence=["#2ecc71","#e74c3c"],
            title="🚨 Countries with Heat Alert Systems", hole=0.5
        )
        fig_alert.update_layout(paper_bgcolor="#0e1117", font_color="white")
        st.plotly_chart(fig_alert, use_container_width=True)

    with col4:
        fig_water = px.bar(
            filtered.sort_values("water_stations", ascending=False),
            x="country", y="water_stations",
            color="water_stations",
            color_continuous_scale=["#74b9ff","#0984e3","#2d3436"],
            title="💧 Water Stations Deployed by Country",
            text="water_stations"
        )
        fig_water.update_traces(texttemplate="%{text:,}", textposition="outside")
        fig_water.update_layout(
            paper_bgcolor="#0e1117", plot_bgcolor="#0e1117", font_color="white",
            xaxis=dict(gridcolor="#333", tickangle=-30),
            yaxis=dict(gridcolor="#333"), coloraxis_showscale=False
        )
        st.plotly_chart(fig_water, use_container_width=True)

    st.markdown("### 🤝 How Can We Help?")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("""<div class="insight-box"><b>🏛️ Governments</b><br><br>
        • Expand cooling centre networks<br>
        • Deploy mobile water stations<br>
        • Emergency pay for outdoor workers<br>
        • Enforce outdoor work bans above 40°C</div>""", unsafe_allow_html=True)
    with col_b:
        st.markdown("""<div class="insight-box"><b>🏥 Health Services</b><br><br>
        • Pre-position IV fluids & cooling equipment<br>
        • Create heat stroke fast-track units<br>
        • Proactive outreach to elderly (65+)<br>
        • Train community volunteers</div>""", unsafe_allow_html=True)
    with col_c:
        st.markdown("""<div class="insight-box"><b>👤 Citizens</b><br><br>
        • Check on elderly neighbours daily<br>
        • Avoid outdoors 11am–5pm<br>
        • Hydrate every 20 minutes<br>
        • Call 112 (EU emergency) for heat stroke</div>""", unsafe_allow_html=True)