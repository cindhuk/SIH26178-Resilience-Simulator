import streamlit as st
from datetime import datetime

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="SIH26178 Resilience Simulator",
    page_icon="🛡️",
    layout="wide"
)

# =========================================================
# SESSION STATE
# =========================================================

if "network_online" not in st.session_state:
    st.session_state.network_online = True

if "queued_alerts" not in st.session_state:
    st.session_state.queued_alerts = []

if "synced_alerts" not in st.session_state:
    st.session_state.synced_alerts = []

# =========================================================
# HEADER
# =========================================================

st.title("🛡️ SIH26178 — Resilience Simulator")

st.write(
    "Software demonstration of edge-first hazard detection, "
    "network failure handling and critical-alert synchronization."
)

st.divider()

# =========================================================
# SYSTEM STATUS
# =========================================================

st.subheader("System Status")

status1, status2, status3, status4 = st.columns(4)

with status1:
    st.metric("Edge Intelligence", "ACTIVE")

with status2:
    st.metric(
        "Network",
        "ONLINE"
        if st.session_state.network_online
        else "OFFLINE"
    )

with status3:
    st.metric(
        "Local Detection",
        "ACTIVE"
    )

with status4:
    st.metric(
        "Queued Alerts",
        len(st.session_state.queued_alerts)
    )

# =========================================================
# ENVIRONMENTAL INPUTS
# =========================================================

st.subheader("🌦️ Environmental Inputs")

col1, col2, col3 = st.columns(3)

with col1:
    water_level = st.slider(
        "Water Level (cm)",
        0,
        100,
        20
    )

with col2:
    rainfall = st.selectbox(
        "Rainfall Intensity",
        ["LOW", "MEDIUM", "HIGH"]
    )

with col3:
    pm25 = st.slider(
        "PM2.5 (µg/m³)",
        0,
        300,
        30
    )

# =========================================================
# DEMONSTRATION RISK ENGINE
# =========================================================

def calculate_risk(water, rain, pm):

    score = 0

    # Water level
    if water >= 70:
        score += 3
    elif water >= 40:
        score += 2
    elif water >= 20:
        score += 1

    # Rainfall
    if rain == "HIGH":
        score += 2
    elif rain == "MEDIUM":
        score += 1

    # PM2.5
    if pm >= 150:
        score += 2
    elif pm >= 75:
        score += 1

    # Risk classification
    if score >= 5:
        return "HIGH"

    elif score >= 3:
        return "MEDIUM"

    else:
        return "LOW"


risk = calculate_risk(
    water_level,
    rainfall,
    pm25
)

# =========================================================
# RISK DISPLAY
# =========================================================

st.subheader("🧠 Local Risk Analysis")

risk_col1, risk_col2 = st.columns(2)

with risk_col1:
    st.metric(
        "Current Risk",
        risk
    )

with risk_col2:
    st.metric(
        "Processing",
        "LOCAL"
    )

# =========================================================
# ALERT GENERATION
# =========================================================

if risk == "HIGH":

    st.error(
        "🚨 HIGH-RISK ENVIRONMENTAL CONDITION DETECTED"
    )

    alert = {
        "time": datetime.now().strftime("%H:%M:%S"),
        "hazard": "Environmental Hazard",
        "risk": risk,
        "water": water_level,
        "rain": rainfall,
        "pm25": pm25
    }

    # -----------------------------------------------------
    # NETWORK ONLINE
    # -----------------------------------------------------

    if st.session_state.network_online:

        st.success(
            "📡 Network available — critical alert can be transmitted."
        )

    # -----------------------------------------------------
    # NETWORK OFFLINE
    # -----------------------------------------------------

    else:

        if alert not in st.session_state.queued_alerts:

            st.session_state.queued_alerts.append(
                alert
            )

        st.warning(
            "📦 Network unavailable. "
            "Critical alert queued for later synchronization."
        )

elif risk == "MEDIUM":

    st.warning(
        "⚠️ MEDIUM-RISK CONDITION DETECTED"
    )

else:

    st.success(
        "✅ LOW-RISK CONDITION"
    )

# =========================================================
# RESILIENCE CONTROL
# =========================================================

st.divider()

st.subheader("📡 Resilience Control")

if st.session_state.network_online:

    st.success(
        "🟢 NETWORK ONLINE"
    )

    if st.button(
        "🔴 SIMULATE NETWORK FAILURE",
        use_container_width=True
    ):

        st.session_state.network_online = False

        st.rerun()

else:

    st.error(
        "🔴 NETWORK OFFLINE"
    )

    st.write(
        "Backhaul connectivity is unavailable."
    )

    if st.button(
        "🟢 RESTORE NETWORK",
        use_container_width=True
    ):

        st.session_state.network_online = True

        # Synchronize queued alerts
        if st.session_state.queued_alerts:

            st.session_state.synced_alerts.extend(
                st.session_state.queued_alerts
            )

            st.session_state.queued_alerts = []

        st.rerun()

# =========================================================
# RESILIENCE DASHBOARD
# =========================================================

st.divider()

st.subheader("🛡️ Resilience Dashboard")

r1, r2, r3, r4 = st.columns(4)

with r1:

    st.metric(
        "Edge Intelligence",
        "ACTIVE"
    )

with r2:

    st.metric(
        "Local Detection",
        "ACTIVE"
    )

with r3:

    st.metric(
        "Backhaul",
        "AVAILABLE"
        if st.session_state.network_online
        else "UNAVAILABLE"
    )

with r4:

    st.metric(
        "Queued Alerts",
        len(st.session_state.queued_alerts)
    )

# =========================================================
# QUEUED ALERTS
# =========================================================

if st.session_state.queued_alerts:

    st.divider()

    st.subheader(
        "📦 Critical Alerts Waiting for Synchronization"
    )

    for i, alert in enumerate(
        st.session_state.queued_alerts,
        start=1
    ):

        st.write(
            f"Alert {i} | "
            f"Time: {alert['time']} | "
            f"Risk: {alert['risk']} | "
            f"Water: {alert['water']} cm | "
            f"Rain: {alert['rain']} | "
            f"PM2.5: {alert['pm25']}"
        )

# =========================================================
# SYNCHRONIZED ALERTS
# =========================================================

if st.session_state.synced_alerts:

    st.divider()

    st.subheader(
        "🔄 Synchronized Alerts"
    )

    st.success(
        f"{len(st.session_state.synced_alerts)} "
        "critical alert(s) synchronized after network recovery."
    )

    for i, alert in enumerate(
        st.session_state.synced_alerts,
        start=1
    ):

        st.write(
            f"Alert {i} | "
            f"Time: {alert['time']} | "
            f"Risk: {alert['risk']} | "
            f"Water: {alert['water']} cm | "
            f"Rain: {alert['rain']} | "
            f"PM2.5: {alert['pm25']}"
        )

# =========================================================
# HOW RESILIENCE WORKS
# =========================================================

st.divider()

st.subheader(
    "How Resilience Works"
)

st.markdown(
    """
### 🟢 Normal Operation

**Environmental Inputs → Local Risk Analysis → Network → Alert Transmission**

### 🔴 Network Failure

**Environmental Inputs → Local Risk Analysis → Local Alert → Alert Queue**

### 🔄 Network Recovery

**Network Restored → Queued Critical Alert → Synchronization**
"""
)

# =========================================================
# DISCLAIMER
# =========================================================

st.divider()

st.caption(
    "Software demonstration for SIH26178. "
    "The current risk engine uses demonstration rules and "
    "is not a validated machine-learning model."
)
