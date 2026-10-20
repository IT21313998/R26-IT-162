"""
generate_presentation.py
Generates a unified, executive-grade 16:9 PowerPoint (.pptx) and matching Presentation PDF (.pdf)
for SLIIT Final Year Research Defense CDAP R26-IT-162.

Unifies Component A (Student A: Rasara S.H.K - IT21313998) and
Component B (Student B: U.H.K Sankalana - IT22236814) into one cohesive,
highly professional visual standard with an in-depth commercialization section.
"""

import os
import sys
import pptx
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

# ReportLab imports for landscape PDF generation
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# ==============================================================================
# COLOR PALETTE CONSTANTS
# ==============================================================================
C_BG_DARK     = RGBColor(11, 19, 37)     # #0B1325 (Deep Slate Navy)
C_CARD_BG     = RGBColor(19, 31, 58)     # #131F3A (Elevated Card)
C_CARD_BORDER = RGBColor(38, 56, 95)     # #26385F (Card Border)
C_CYAN        = RGBColor(14, 165, 233)   # #0EA5E9 (Primary Accent)
C_WATER_BLUE  = RGBColor(2, 132, 199)    # #0284C7 (Hydrology Blue)
C_EMERALD     = RGBColor(16, 185, 129)   # #10B981 (Success / Safe)
C_AMBER       = RGBColor(245, 158, 11)   # #F59E0B (Warning)
C_ROSE        = RGBColor(239, 68, 68)    # #EF4444 (Danger / Inundation)
C_WHITE       = RGBColor(255, 255, 255)  # Text Pure White
C_MUTED       = RGBColor(148, 163, 184)  # #94A3B8 (Subtext)
C_LIGHT_BLUE  = RGBColor(224, 242, 254)  # #E0F2FE (Pill Text)


def create_unified_pptx(output_pptx="SLIIT_R26_IT_162_Final_Presentation.pptx"):
    print(f"[*] Building 16:9 Widescreen PPTX: {output_pptx}")
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide):
        bg_shape = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5)
        )
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = C_BG_DARK
        bg_shape.line.fill.background()
        return bg_shape

    def add_header(slide, tag_text, title_text, subtitle_text=""):
        tag_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(8), Inches(0.35))
        tf_tag = tag_box.text_frame
        tf_tag.word_wrap = True
        tf_tag.margin_left = tf_tag.margin_top = tf_tag.margin_right = tf_tag.margin_bottom = 0
        p_tag = tf_tag.paragraphs[0]
        p_tag.text = tag_text.upper()
        p_tag.font.name = "Arial"
        p_tag.font.size = Pt(10)
        p_tag.font.bold = True
        p_tag.font.color.rgb = C_CYAN

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.75), Inches(11.7), Inches(0.7))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        tf_title.margin_left = tf_title.margin_top = tf_title.margin_right = tf_title.margin_bottom = 0
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.name = "Arial"
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = C_WHITE

        if subtitle_text:
            sub_box = slide.shapes.add_textbox(Inches(0.8), Inches(1.4), Inches(11.7), Inches(0.45))
            tf_sub = sub_box.text_frame
            tf_sub.word_wrap = True
            tf_sub.margin_left = tf_sub.margin_top = tf_sub.margin_right = tf_sub.margin_bottom = 0
            p_sub = tf_sub.paragraphs[0]
            p_sub.text = subtitle_text
            p_sub.font.name = "Arial"
            p_sub.font.size = Pt(12)
            p_sub.font.color.rgb = C_MUTED

    def add_footer(slide, slide_num, total_slides=13):
        foot_box = slide.shapes.add_textbox(Inches(0.8), Inches(7.0), Inches(11.7), Inches(0.3))
        tf = foot_box.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = f"SLIIT CDAP R26-IT-162 | FloodSense AI (Kelani River Basin Early Warning) | Slide {slide_num} of {total_slides}"
        p.font.name = "Arial"
        p.font.size = Pt(9)
        p.font.color.rgb = C_MUTED

    def add_card(slide, left, top, width, height, bg_rgb=C_CARD_BG, border_rgb=C_CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_rgb
        card.line.color.rgb = border_rgb
        card.line.width = Pt(1.2)
        return card

    # ==========================================================================
    # SLIDE 1: TITLE SLIDE
    # ==========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    tbox = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.333), Inches(2.2))
    tf = tbox.text_frame
    tf.word_wrap = True
    
    p0 = tf.paragraphs[0]
    p0.text = "SLIIT FACULTY OF COMPUTING | CDAP RESEARCH PROJECT R26-IT-162"
    p0.font.name = "Arial"
    p0.font.size = Pt(12)
    p0.font.bold = True
    p0.font.color.rgb = C_CYAN
    p0.space_after = Pt(10)

    p1 = tf.add_paragraph()
    p1.text = "FloodSense AI: Intelligent IoT Microclimate Sensing & Dual-Stage Predictive Flood Inundation Modeling"
    p1.font.name = "Arial"
    p1.font.size = Pt(28)
    p1.font.bold = True
    p1.font.color.rgb = C_WHITE
    p1.space_after = Pt(12)

    p2 = tf.add_paragraph()
    p2.text = "Hyperlocal Rainfall Forecasting & Distance-Based Dynamic Risk Scoring for Kelani River Basin Communities"
    p2.font.name = "Arial"
    p2.font.size = Pt(14)
    p2.font.color.rgb = C_MUTED

    # Student A Card
    add_card(s1, Inches(1.0), Inches(4.0), Inches(5.4), Inches(2.5))
    c_a = s1.shapes.add_textbox(Inches(1.2), Inches(4.15), Inches(5.0), Inches(2.2))
    tfa = c_a.text_frame
    tfa.word_wrap = True
    
    pa1 = tfa.paragraphs[0]
    pa1.text = "STUDENT A: EMBEDDED IOT & RAINFALL ML ENGINE"
    pa1.font.name = "Arial"
    pa1.font.size = Pt(10)
    pa1.font.bold = True
    pa1.font.color.rgb = C_WATER_BLUE

    pa2 = tfa.add_paragraph()
    pa2.text = "Rasara S.H.K. (IT21313998)"
    pa2.font.name = "Arial"
    pa2.font.size = Pt(16)
    pa2.font.bold = True
    pa2.font.color.rgb = C_WHITE
    pa2.space_after = Pt(6)

    pa3 = tfa.add_paragraph()
    pa3.text = "• Hardware: ESP32 Microcontroller + Calibrated Tipping Bucket Rain Gauge\n• Cloud Messaging: Lightweight MQTT Telemetry over HiveMQ Cloud Broker\n• Atmospheric Fusion: 14 Open-Meteo Synoptic Weather Variables\n• ML Models: LightGBM & XGBoost Multi-Horizon Forecasting (24h, 48h, 72h)"
    pa3.font.name = "Arial"
    pa3.font.size = Pt(10)
    pa3.font.color.rgb = C_MUTED

    # Student B Card
    add_card(s1, Inches(6.8), Inches(4.0), Inches(5.4), Inches(2.5))
    c_b = s1.shapes.add_textbox(Inches(7.0), Inches(4.15), Inches(5.0), Inches(2.2))
    tfb = c_b.text_frame
    tfb.word_wrap = True
    
    pb1 = tfb.paragraphs[0]
    pb1.text = "STUDENT B: TWO-STAGE FLOOD RISK & SAAS UI"
    pb1.font.name = "Arial"
    pb1.font.size = Pt(10)
    pb1.font.bold = True
    pb1.font.color.rgb = C_EMERALD

    pb2 = tfb.add_paragraph()
    pb2.text = "U.H.K. Sankalana (IT22236814)"
    pb2.font.name = "Arial"
    pb2.font.size = Pt(16)
    pb2.font.bold = True
    pb2.font.color.rgb = C_WHITE
    pb2.space_after = Pt(6)

    pb3 = tfb.add_paragraph()
    pb3.text = "• Risk Algorithm: Distance-Based Dynamic Flood Risk Personalization (DFRS)\n• ML Pipeline: Two-Stage XGBoost (Stage 1A Classifier, 1B Risk Regressor)\n• Hydrology Output: Stage 2 Multi-Output (Inundation Arrival Time & Water Depth)\n• Web Interface: Modern React Dashboard with Trilingual Notification Alerts"
    pb3.font.name = "Arial"
    pb3.font.size = Pt(10)
    pb3.font.color.rgb = C_MUTED

    add_footer(s1, 1)

    # ==========================================================================
    # SLIDE 2: PROBLEM STATEMENT
    # ==========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Problem Context & Socio-Economic Impact", "The Kelani River Basin Flood Crisis & The Early Warning Deficit", "500,000+ vulnerable citizens face recurring catastrophic monsoonal inundation with inadequate warning lead time")

    metrics = [
        ("500,000+", "Vulnerable Citizens", "Across Colombo, Gampaha & Kegalle", C_CYAN),
        ("LKR 50B+", "Annual Economic Loss", "Infrastructure, property & crop damage", C_ROSE),
        ("300,000+", "Displaced Annually", "Major events in 2016, 2021 & 2024", C_AMBER),
        ("6–12 Hours", "Current Warning Gap", "Synoptic forecasts lack micro-catchment resolution", C_WATER_BLUE)
    ]
    for idx, (m_val, m_title, m_desc, m_col) in enumerate(metrics):
        cx = Inches(0.8 + idx * 2.98)
        add_card(s2, cx, Inches(2.0), Inches(2.8), Inches(1.6))
        tb = s2.shapes.add_textbox(cx + Inches(0.15), Inches(2.1), Inches(2.5), Inches(1.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = m_val
        p1.font.name = "Arial"
        p1.font.size = Pt(24)
        p1.font.bold = True
        p1.font.color.rgb = m_col
        p2 = tf.add_paragraph()
        p2.text = m_title
        p2.font.name = "Arial"
        p2.font.size = Pt(11)
        p2.font.bold = True
        p2.font.color.rgb = C_WHITE
        p3 = tf.add_paragraph()
        p3.text = m_desc
        p3.font.name = "Arial"
        p3.font.size = Pt(9)
        p3.font.color.rgb = C_MUTED

    add_card(s2, Inches(0.8), Inches(3.9), Inches(5.7), Inches(2.8))
    tb_exist = s2.shapes.add_textbox(Inches(1.0), Inches(4.05), Inches(5.3), Inches(2.5))
    tf_e = tb_exist.text_frame
    tf_e.word_wrap = True
    pe1 = tf_e.paragraphs[0]
    pe1.text = "LIMITATIONS OF CURRENT DISASTER SYSTEMS"
    pe1.font.name = "Arial"
    pe1.font.size = Pt(12)
    pe1.font.bold = True
    pe1.font.color.rgb = C_ROSE
    pe2 = tf_e.add_paragraph()
    pe2.text = "• Coarse Spatial Resolution: 25 km synoptic weather grids miss localized convective micro-catchment cloudbursts.\n• Manual Gauge Reporting: Gauge readings are collected manually every 6–12 hours, creating fatal latency.\n• Binary Blanket Alerts: DMC alerts simply state 'Kelani Basin Flood Alert' without telling a family if water will reach their specific doorstep or in how many hours.\n• No Water Depth or Arrival Estimation: No actionable metrics for evacuation planning or asset protection."
    pe2.font.name = "Arial"
    pe2.font.size = Pt(10.5)
    pe2.font.color.rgb = C_MUTED

    add_card(s2, Inches(6.8), Inches(3.9), Inches(5.7), Inches(2.8))
    tb_sol = s2.shapes.add_textbox(Inches(7.0), Inches(4.05), Inches(5.3), Inches(2.5))
    tf_s = tb_sol.text_frame
    tf_s.word_wrap = True
    ps1 = tf_s.paragraphs[0]
    ps1.text = "OUR INTEGRATED AI & IOT PARADIGM"
    ps1.font.name = "Arial"
    ps1.font.size = Pt(12)
    ps1.font.bold = True
    ps1.font.color.rgb = C_EMERALD
    ps2 = tf_s.add_paragraph()
    ps2.text = "• Sub-Kilometer Microclimate Sensing: Real-time calibrated tipping buckets streaming live rain intensity via MQTT.\n• Atmospheric Fusion AI: Fuses 14 synoptic weather variables to project 24h, 48h, and 72h antecedent rainfall depths.\n• Two-Stage Inundation Intelligence: Evaluates localized occurrence (Yes/No), continuous risk score (0–100), arrival time (hours), and inundation depth (meters).\n• Trilingual Decision Support: Automated alerts dispatched in Sinhala, Tamil, and English with community evacuation SOPs."
    ps2.font.name = "Arial"
    ps2.font.size = Pt(10.5)
    ps2.font.color.rgb = C_MUTED

    add_footer(s2, 2)

    # ==========================================================================
    # SLIDE 3: REVIEWER ENHANCEMENTS
    # ==========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Reviewer Feedback & System Evolution", "How We Addressed Panel Comments & Upgraded the Research", "Systematic progression from a basic monitoring prototype to an enterprise-grade AI flood early warning system")

    upgrades = [
        ("01. DETECTION & SENSING", "From: Single sensor & basic monitoring", "To: Multi-factor IoT sensing array (calibrated tipping bucket, reed switch debouncing ISR, Open-Meteo 14-variable live atmospheric fusion)."),
        ("02. DATA PIPELINE", "From: Manual logs & once-a-day polling", "To: Sub-second MQTT streaming via HiveMQ Cloud Broker with local non-volatile buffering and automatic reconnect watchdog."),
        ("03. PREDICTIVE CAPABILITY", "From: Binary flood alerts (Yes / No)", "To: Dual-stage ML pipeline providing continuous risk score (0–100%), arrival time in hours, and water height with cm precision."),
        ("04. TARGETED BENEFICIARIES", "From: Generic text notifications", "To: Personalized Distance-Based Dynamic Risk Scoring (DFRS) with automated trilingual notifications (Sinhala, Tamil, English).")
    ]
    for idx, (step_tag, f_text, t_text) in enumerate(upgrades):
        top_y = Inches(2.0 + idx * 1.18)
        add_card(s3, Inches(0.8), top_y, Inches(11.7), Inches(1.05))
        tb = s3.shapes.add_textbox(Inches(1.0), top_y + Inches(0.08), Inches(11.3), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = step_tag
        p1.font.name = "Arial"
        p1.font.size = Pt(9.5)
        p1.font.bold = True
        p1.font.color.rgb = C_CYAN
        p2 = tf.add_paragraph()
        p2.text = f"{f_text}  ➔  {t_text}"
        p2.font.name = "Arial"
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = C_WHITE

    add_footer(s3, 3)

    # ==========================================================================
    # SLIDE 4: SYSTEM ARCHITECTURE
    # ==========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "System Architecture & Data Flow", "The Integrated Symbiotic Pipeline: Sensor to Inundation Decision", "Seamless cross-tier data pipeline connecting Student A's IoT & ML engine with Student B's flood risk models")

    stages = [
        ("LAYER 1: SENSING & TELEMETRY", "Component A (Rasara)", [
            "• ESP32 Microcontroller (GPIO 4)",
            "• Tipping Bucket (0.2 mm/tip)",
            "• 100 ms Hardware/Software Debounce",
            "• HiveMQ MQTT Cloud Broker",
            "• JSON Payload Serialization"
        ], C_WATER_BLUE),
        ("LAYER 2: FUSION & RAINFALL ML", "Component A (Rasara)", [
            "• Open-Meteo Live Synoptic API",
            "• 14 Atmospheric Variables (CAPE, RH)",
            "• 168h Antecedent Rolling Buffers",
            "• LightGBM Multi-Horizon Predictor",
            "• Forecasts: 24h, 48h, 72h Depths"
        ], C_CYAN),
        ("LAYER 3: TWO-STAGE FLOOD ML", "Component B (Sankalana)", [
            "• Stage 1A: XGBoost Classifier",
            "• Evaluates Flood Occurrence (Yes/No)",
            "• Stage 1B: XGBoost Regressor (0-100)",
            "• Stage 2: Multi-Output Regressor",
            "• Predicts: Arrival Time & Water Depth"
        ], C_EMERALD),
        ("LAYER 4: DECISION SUPPORT", "Component B (Sankalana)", [
            "• Distance-Based Proximity Engine",
            "• Modern React Dashboard UI",
            "• Live SVG Risk Dials & Audits",
            "• Automated Trilingual Alert Dispatch",
            "• DMC Civil Defense SOP Guidance"
        ], C_AMBER),
    ]
    for idx, (layer_title, author_tag, items, col) in enumerate(stages):
        cx = Inches(0.8 + idx * 2.98)
        add_card(s4, cx, Inches(2.0), Inches(2.8), Inches(4.7))
        tb = s4.shapes.add_textbox(cx + Inches(0.15), Inches(2.15), Inches(2.5), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = layer_title
        p1.font.name = "Arial"
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = col
        p2 = tf.add_paragraph()
        p2.text = author_tag
        p2.font.name = "Arial"
        p2.font.size = Pt(9)
        p2.font.color.rgb = C_LIGHT_BLUE
        p2.space_after = Pt(10)
        for it in items:
            p = tf.add_paragraph()
            p.text = it
            p.font.name = "Arial"
            p.font.size = Pt(10)
            p.font.color.rgb = C_MUTED
            p.space_after = Pt(4)

    add_footer(s4, 4)

    # ==========================================================================
    # SLIDE 5: COMPONENT A — IOT HARDWARE
    # ==========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Component A | Rasara S.H.K. (IT21313998)", "Embedded IoT Microclimate Sensing & Edge Telemetry Firmware", "High-frequency rainfall pulse detection with hardware debouncing and resilient cloud messaging")

    add_card(s5, Inches(0.8), Inches(2.0), Inches(3.7), Inches(4.7))
    tb1 = s5.shapes.add_textbox(Inches(0.95), Inches(2.15), Inches(3.4), Inches(4.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "HARDWARE ARCHITECTURE"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.space_after = Pt(8)
    tf1.add_paragraph().text = "• MCU: ESP32 dual-core Xtensa 32-bit LX6 running at 240 MHz with 520 KB SRAM."
    tf1.add_paragraph().text = "• Rain Sensor: Dual-chamber tipping bucket rain collector with magnetic reed switch."
    tf1.add_paragraph().text = "• Physical Calibration: 0.20 mm displacement per mechanical tip (funnel area 32,429 mm²)."
    tf1.add_paragraph().text = "• Microclimate Module: DHT22 / BME280 temperature and relative humidity monitoring."
    tf1.add_paragraph().text = "• Power Subsystem: 3.7V 18650 Li-ion battery with 6V 5W solar panel and TP4056 charge IC."
    for para in tf1.paragraphs[1:]:
        para.font.name = "Arial"
        para.font.size = Pt(10)
        para.font.color.rgb = C_MUTED
        para.space_after = Pt(4)

    add_card(s5, Inches(4.8), Inches(2.0), Inches(3.7), Inches(4.7))
    tb2 = s5.shapes.add_textbox(Inches(4.95), Inches(2.15), Inches(3.4), Inches(4.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "SIGNAL PROCESSING & ISR"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_WATER_BLUE
    p.space_after = Pt(8)
    tf2.add_paragraph().text = "• Interrupt Service Routine (ISR): Bound to GPIO 4 (FALLING edge), executed in high-speed IRAM."
    tf2.add_paragraph().text = "• Software Debouncing: Enforces a 100 ms threshold to eliminate reed switch contact chatter oscillations."
    tf2.add_paragraph().text = "• Intensity Calculation: Computes rainfall intensity dynamically based on pulse arrival frequency."
    tf2.add_paragraph().text = "• Median Filter: 5-sample moving median filter prevents false positive spikes from debris."
    tf2.add_paragraph().text = "• Watchdog Timer: Automatic hardware recovery resets the microcontroller if network hangs."
    for para in tf2.paragraphs[1:]:
        para.font.name = "Arial"
        para.font.size = Pt(10)
        para.font.color.rgb = C_MUTED
        para.space_after = Pt(4)

    add_card(s5, Inches(8.8), Inches(2.0), Inches(3.7), Inches(4.7))
    tb3 = s5.shapes.add_textbox(Inches(8.95), Inches(2.15), Inches(3.4), Inches(4.4))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "MQTT CLOUD TELEMETRY"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    p.space_after = Pt(8)
    tf3.add_paragraph().text = "• Protocol: MQTT v3.1.1 (lightweight 2-byte header overhead vs 800-byte HTTP REST)."
    tf3.add_paragraph().text = "• Cloud Broker: HiveMQ Cloud cluster (broker.hivemq.com:1883, topic: 'Smart Irrigation Hive/data')."
    tf3.add_paragraph().text = "• Telemetry Payload: Serialized JSON with device ID, tip count, rainfall rate, temperature & battery."
    tf3.add_paragraph().text = "• Local Storage Fallback: Non-volatile SPIFFS flash logs data if cellular connection drops."
    tf3.add_paragraph().text = "• Ingestion Latency: Sub-second (typically <280 ms) cloud ingestion from edge to backend."
    for para in tf3.paragraphs[1:]:
        para.font.name = "Arial"
        para.font.size = Pt(10)
        para.font.color.rgb = C_MUTED
        para.space_after = Pt(4)

    add_footer(s5, 5)

    # ==========================================================================
    # SLIDE 6: COMPONENT A — RAINFALL ML
    # ==========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Component A | Rasara S.H.K. (IT21313998)", "Multi-Horizon Machine Learning Rainfall Forecasting Engine", "Coupling atmospheric reanalysis with edge telemetry to predict 24h, 48h, and 72h precipitation depths")

    add_card(s6, Inches(0.8), Inches(2.0), Inches(5.7), Inches(4.7))
    tb_m = s6.shapes.add_textbox(Inches(1.0), Inches(2.15), Inches(5.3), Inches(4.4))
    tfm = tb_m.text_frame
    tfm.word_wrap = True
    pm = tfm.paragraphs[0]
    pm.text = "DATA FUSION & FEATURE ENGINEERING PIPELINE"
    pm.font.name = "Arial"
    pm.font.size = Pt(12)
    pm.font.bold = True
    pm.font.color.rgb = C_CYAN
    pm.space_after = Pt(8)
    tfm.add_paragraph().text = "• 14 Atmospheric Variables: Real-time ECMWF/GFS grids from Open-Meteo (CAPE, 2m temp, surface pressure, relative humidity, cloud cover, dew point)."
    tfm.add_paragraph().text = "• Wind Vector Decomposition: 10m wind speed and direction transformed into orthogonal vectors u = -s·sin(θ) and v = -s·cos(θ) to capture monsoonal moisture advection."
    tfm.add_paragraph().text = "• Antecedent Rolling Windows: 1h, 3h, 6h, 12h, 24h, 48h, 72h, and 7-day cumulative rainfall and moving variances."
    tfm.add_paragraph().text = "• Antecedent Precipitation Index (API): Models soil moisture depletion across continuous days (recession constant k = 0.88)."
    tfm.add_paragraph().text = "• Cyclical Manifold Encodings: Sine and cosine harmonics encode day-of-year and hour-of-day, preserving monsoonal continuity."
    tfm.add_paragraph().text = "• Data Leakage Prevention: Evaluated strictly with TimeSeriesSplit (n_splits=5); zero lookahead bias."
    for p in tfm.paragraphs[1:]:
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.color.rgb = C_MUTED
        p.space_after = Pt(4)

    add_card(s6, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.7))
    tb_b = s6.shapes.add_textbox(Inches(7.0), Inches(2.15), Inches(5.3), Inches(4.4))
    tfb = tb_b.text_frame
    tfb.word_wrap = True
    pb = tfb.paragraphs[0]
    pb.text = "MODEL BENCHMARKS & EVALUATION RESULTS"
    pb.font.name = "Arial"
    pb.font.size = Pt(12)
    pb.font.bold = True
    pb.font.color.rgb = C_EMERALD
    pb.space_after = Pt(8)
    tfb.add_paragraph().text = "Comparative Multi-Horizon Benchmark (Day 1 / 24h Horizon):"
    tfb.add_paragraph().text = "🏆 LightGBM Regressor: R² = 0.841 | MAE = 2.84 mm | RMSE = 4.12 mm"
    tfb.add_paragraph().text = "🥈 XGBoost Regressor: R² = 0.835 | MAE = 2.98 mm | RMSE = 4.25 mm"
    tfb.add_paragraph().text = "🥉 Random Forest: R² = 0.792 | MAE = 3.65 mm | RMSE = 5.10 mm"
    tfb.add_paragraph().text = "• Ridge Linear Baseline: R² = 0.648 | MAE = 5.82 mm | RMSE = 7.40 mm"
    tfb.add_paragraph().text = "\nKey Research Findings:"
    tfb.add_paragraph().text = "• LightGBM's Gradient-based One-Side Sampling (GOSS) and Exclusive Feature Bundling (EFB) achieved 30ms inference latency on commodity CPUs."
    tfb.add_paragraph().text = "• Rain Occurrence Classification: F1-score of 0.912 and ROC-AUC of 0.945."
    tfb.add_paragraph().text = "• Automated Payload Handoff: Model aggregates 7-day total and peak intensity, feeding directly into Student B's flood model."
    for p in tfb.paragraphs[1:]:
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.color.rgb = C_WHITE if "LightGBM" in p.text else C_MUTED
        p.space_after = Pt(3)

    add_footer(s6, 6)

    # ==========================================================================
    # SLIDE 7: COMPONENT B — TWO-STAGE FLOOD ML
    # ==========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Component B | U.H.K. Sankalana (IT22236814)", "Two-Stage Machine Learning Dynamic Flood Risk & Inundation Model", "Combining hydro-topographic vectors with rainfall predictions to compute occurrence, risk score, arrival time, and depth")

    add_card(s7, Inches(0.8), Inches(2.0), Inches(3.7), Inches(4.7))
    t1 = s7.shapes.add_textbox(Inches(0.95), Inches(2.15), Inches(3.4), Inches(4.4))
    tf1 = t1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "STAGE 1A: BINARY CLASSIFIER"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.space_after = Pt(6)
    tf1.add_paragraph().text = "• Model: XGBoost Classifier (stage1_classifier.json)"
    tf1.add_paragraph().text = "• Task: Evaluates whether a flood will physically occur (Yes / No)."
    tf1.add_paragraph().text = "• Bayesian Posterior: Computes calibrated probability P(Flood)."
    tf1.add_paragraph().text = "• F1-Score: 0.941 across 10-year historical Kelani validation callset."
    tf1.add_paragraph().text = "• Top Split Features: 7-day rainfall total and peak storm intensity (from Student A)."
    for p in tf1.paragraphs[1:]:
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.color.rgb = C_MUTED
        p.space_after = Pt(4)

    add_card(s7, Inches(4.8), Inches(2.0), Inches(3.7), Inches(4.7))
    t2 = s7.shapes.add_textbox(Inches(4.95), Inches(2.15), Inches(3.4), Inches(4.4))
    tf2 = t2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "STAGE 1B: RISK REGRESSOR"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p.space_after = Pt(6)
    tf2.add_paragraph().text = "• Model: XGBoost Regressor (stage1_risk_regressor.json)"
    tf2.add_paragraph().text = "• Task: Produces continuous 0 to 100 Flood Risk Score."
    tf2.add_paragraph().text = "• RMSE: 3.12 (on 0–100 scale)."
    tf2.add_paragraph().text = "• Severity Tiers:"
    tf2.add_paragraph().text = "  - Very High: Score ≥ 70 (Evacuation)"
    tf2.add_paragraph().text = "  - High: Score 50 – 69 (Severe Alert)"
    tf2.add_paragraph().text = "  - Moderate: Score 30 – 49 (Monitor)"
    tf2.add_paragraph().text = "  - Low: Score < 30 (Baseline Safe)"
    for p in tf2.paragraphs[1:]:
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.color.rgb = C_MUTED
        p.space_after = Pt(3)

    add_card(s7, Inches(8.8), Inches(2.0), Inches(3.7), Inches(4.7))
    t3 = s7.shapes.add_textbox(Inches(8.95), Inches(2.15), Inches(3.4), Inches(4.4))
    tf3 = t3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "STAGE 2: MULTI-OUTPUT"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_ROSE
    p.space_after = Pt(6)
    tf3.add_paragraph().text = "• Model: MultiOutput XGBoost Regressor (Executes only if Stage 1A = Yes)"
    tf3.add_paragraph().text = "• Metric 1: Inundation Arrival Time (hours until wavefront hits community locus)."
    tf3.add_paragraph().text = "• Metric 2: Peak Inundation Height (water depth in meters above ground level)."
    tf3.add_paragraph().text = "• Physical Damping: Integrates terrain elevation, river distance, and soil permeability."
    for p in tf3.paragraphs[1:]:
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.color.rgb = C_MUTED
        p.space_after = Pt(4)

    add_footer(s7, 7)

    # ==========================================================================
    # SLIDE 8: COMPONENT B — DFRS & REACT UI
    # ==========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Component B | U.H.K. Sankalana (IT22236814)", "Distance-Based Dynamic Flood Risk Personalization (DFRS)", "Hyperlocal spatial proximity modeling, executive React dashboard UI, and trilingual community alerts")

    add_card(s8, Inches(0.8), Inches(2.0), Inches(5.7), Inches(4.7))
    t_dfrs = s8.shapes.add_textbox(Inches(1.0), Inches(2.15), Inches(5.3), Inches(4.4))
    tfd = t_dfrs.text_frame
    tfd.word_wrap = True
    p = tfd.paragraphs[0]
    p.text = "DISTANCE-BASED DYNAMIC FLOOD RISK (DFRS)"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_WATER_BLUE
    p.space_after = Pt(8)
    tfd.add_paragraph().text = "• Proximity Decay Formulation: Risk score dynamically scales as Euclidean distance to the active river channel decreases."
    tfd.add_paragraph().text = "• Geospatial Feature Integration: Couples elevation (DEM/SRTM), soil classification (Clay vs Sandy), and land cover (Urban vs Agricultural)."
    tfd.add_paragraph().text = "• Sedawatta / Grandpass Reach (High Risk): River distance = 45m, elevation = 3.2m ➔ Triggers rapid arrival alert (3.4 hours, 3.84m depth)."
    tfd.add_paragraph().text = "• Malabe Elevated Reach (Safe): River distance = 1,250m, elevation = 32m ➔ Low risk score (<25%), normal baseline status."
    for p in tfd.paragraphs[1:]:
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.color.rgb = C_MUTED
        p.space_after = Pt(4)

    add_card(s8, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.7))
    t_dash = s8.shapes.add_textbox(Inches(7.0), Inches(2.15), Inches(5.3), Inches(4.4))
    tfs = t_dash.text_frame
    tfs.word_wrap = True
    p = tfs.paragraphs[0]
    p.text = "EXECUTIVE REACT DASHBOARD & MULTILINGUAL ALERTS"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    p.space_after = Pt(8)
    tfs.add_paragraph().text = "• Responsive Vite React Architecture: Built with Tailwind CSS, Plus Jakarta Sans typography, and SVG semi-circular risk dials."
    tfs.add_paragraph().text = "• Live Backend Health Monitor: Real-time pulsing badge checks Flask ML inference engine (/api/health) on port 5000."
    tfs.add_paragraph().text = "• 1-Click Viva Presets: Instant scenario buttons for Colombo Lower Reach (Sedawatta), Ja-Ela Plain, and Malabe Inland."
    tfs.add_paragraph().text = "• Trilingual Automated Alerts: Dispatches localized emergency directives in Sinhala, Tamil, and English via SMS & push notifications."
    tfs.add_paragraph().text = "• DMC SOP Guidelines: Displays actionable mitigation steps (boat mobilization, electrical de-energizing) based on predicted depth."
    for p in tfs.paragraphs[1:]:
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.color.rgb = C_MUTED
        p.space_after = Pt(4)

    add_footer(s8, 8)

    # ==========================================================================
    # SLIDE 9: INTEGRATION BRIDGE
    # ==========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Cross-System Integration & Data Contract", "How Component A Feeds Component B in Real-Time", "The automated mapping pipeline transforming multi-horizon rainfall forecasts into the 12-feature flood matrix")

    add_card(s9, Inches(0.8), Inches(2.0), Inches(11.7), Inches(4.7))
    tb_int = s9.shapes.add_textbox(Inches(1.0), Inches(2.15), Inches(11.3), Inches(4.4))
    tfi = tb_int.text_frame
    tfi.word_wrap = True
    p = tfi.paragraphs[0]
    p.text = "THE 12-FEATURE DATA HAND-OFF CONTRACT"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.space_after = Pt(6)

    tfi.add_paragraph().text = "Component A (Student A) passes 3 primary dynamic hydrometeorological features via REST API & In-Process Bridge:"
    tfi.add_paragraph().text = "1. rainfall_7d_mm = round(rain_cum72h * 1.8 + rain_24h, 2)  ➔ Cumulative antecedent saturation (200 mm)"
    tfi.add_paragraph().text = "2. monthly_rainfall_mm = round(rain_cum72h * 4.2 + 80.0, 2) ➔ 30-day baseline ground saturation (350 mm)"
    tfi.add_paragraph().text = "3. rainfall_intensity_mmhr = round(iot_rate * 3.5, 2)       ➔ Peak storm cloudburst intensity (15–28 mm/hr)"
    tfi.add_paragraph().text = "\nComponent B (Student B) combines these with 9 geospatial & catchment features:"
    tfi.add_paragraph().text = "• district: Colombo / Gampaha          • latitude & longitude: GPS WGS84 coordinates"
    tfi.add_paragraph().text = "• elevation_m: Topographic elevation   • distance_to_river_m: Proximity to active channel"
    tfi.add_paragraph().text = "• landcover: Urban, Agriculture        • soil_type: Clay, Loamy, Sandy"
    tfi.add_paragraph().text = "• historical_flood_count: DMC records   • river_flow_rate_m3s: Upstream hydrometric discharge"
    tfi.add_paragraph().text = "\nExecution Result:"
    tfi.add_paragraph().text = "➔ Clicking '⚡ Sync IoT Rainfall' in React UI instantly binds Component A's forecast into Component B's Two-Stage XGBoost model, producing Occurrence = YES, Risk = 56.92%, Arrival = 3.41h, Height = 3.84m."
    
    for p in tfi.paragraphs[1:]:
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.color.rgb = C_WHITE if "Clicking" in p.text else C_MUTED
        p.space_after = Pt(3)

    add_footer(s9, 9)

    # ==========================================================================
    # SLIDE 10: USER TESTING
    # ==========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Empirical Validation & Community Field Trials", "Field Testing Across Kelani Riverine Communities & Post-Test Iterations", "Tested over 3 weeks across 3 agricultural riverine locations capturing 12 real monsoon rainfall events")

    add_card(s10, Inches(0.8), Inches(2.0), Inches(3.7), Inches(4.7))
    t1 = s10.shapes.add_textbox(Inches(0.95), Inches(2.15), Inches(3.4), Inches(4.4))
    tf1 = t1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "FIELD TRIAL PROTOCOL"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.space_after = Pt(6)
    tf1.add_paragraph().text = "• Locations: Sedawatta (Lower Reach), Hanwella (Mid Reach), Kaduwela (Lowland Plain)."
    tf1.add_paragraph().text = "• Participants: 15 riverine households, 5 local farmers, 2 local disaster response coordinators."
    tf1.add_paragraph().text = "• Duration: 3-week continuous monitoring period during South-West monsoon burst."
    tf1.add_paragraph().text = "• Events Captured: 12 independent rainfall pulses ranging from 12 mm to 145 mm/day."
    for p in tf1.paragraphs[1:]:
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.color.rgb = C_MUTED
        p.space_after = Pt(4)

    add_card(s10, Inches(4.8), Inches(2.0), Inches(3.7), Inches(4.7))
    t2 = s10.shapes.add_textbox(Inches(4.95), Inches(2.15), Inches(3.4), Inches(4.4))
    tf2 = t2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "USER EVALUATION SCORES"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    p.space_after = Pt(6)
    tf2.add_paragraph().text = "• Overall Satisfaction: 4.4 / 5.0"
    tf2.add_paragraph().text = "• Timeliness of Alert: 4.6 / 5.0 (Average 4.2 hours actionable lead time)."
    tf2.add_paragraph().text = "• Language Clarity: 4.8 / 5.0 (Trilingual Sinhala & Tamil alerts highly praised)."
    tf2.add_paragraph().text = "• Usability of Web UI: 4.3 / 5.0 (Clear color-coded risk dials appreciated by officers)."
    tf2.add_paragraph().text = "• False Alarm Rate: Low (<8.3%), far superior to regional blanket warnings."
    for p in tf2.paragraphs[1:]:
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.color.rgb = C_MUTED
        p.space_after = Pt(4)

    add_card(s10, Inches(8.8), Inches(2.0), Inches(3.7), Inches(4.7))
    t3 = s10.shapes.add_textbox(Inches(8.95), Inches(2.15), Inches(3.4), Inches(4.4))
    tf3 = t3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "POST-TESTING ITERATIONS"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p.space_after = Pt(6)
    tf3.add_paragraph().text = "• Request: Prevent false tip triggers from wind-blown tree debris.\n➔ Action: Added 5-sample median filtering in firmware."
    tf3.add_paragraph().text = "• Request: Adjustable risk sensitivity for elevated farmers.\n➔ Action: Added configurable distance weighting in DFRS."
    tf3.add_paragraph().text = "• Request: Longer off-grid battery resilience in severe overcast.\n➔ Action: Optimized deep sleep cycling, extending battery life to 90 days."
    for p in tf3.paragraphs[1:]:
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_MUTED
        p.space_after = Pt(4)

    add_footer(s10, 10)

    # ==========================================================================
    # SLIDE 11: COMMERCIALIZATION
    # ==========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Commercialization & Market Feasibility", "Business Model, Unit Economics & 3-Year Financial Sustainability", "A high-margin, scalable B2G & B2B SaaS model providing 26x cost disruption over imported telemetry stations")

    add_card(s11, Inches(0.8), Inches(2.0), Inches(3.7), Inches(4.7))
    tb1 = s11.shapes.add_textbox(Inches(0.95), Inches(2.15), Inches(3.4), Inches(4.4))
    tf1 = tb1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    p.text = "MULTI-STREAM REVENUE MODEL"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.space_after = Pt(6)
    tf1.add_paragraph().text = "1. B2G Municipal Contracts (Primary):"
    tf1.add_paragraph().text = "• Annual monitoring & maintenance SLA with Disaster Management Centre (DMC) & Ministry of Irrigation."
    tf1.add_paragraph().text = "• Retainer: LKR 1.5M – 2.5M / year per river basin catchment."
    tf1.add_paragraph().text = "\n2. Insurance Data-as-a-Service (DaaS):"
    tf1.add_paragraph().text = "• Parametric flood risk verification API for insurers (Ceylinco, Sri Lanka Insurance) to validate flood damage claims."
    tf1.add_paragraph().text = "• Fee: LKR 250,000 / month per institutional subscriber."
    tf1.add_paragraph().text = "\n3. B2B Commercial Agriculture:"
    tf1.add_paragraph().text = "• Real-time microclimate soil-moisture feeds for tea/rubber estates in upstream Kegalle."
    for p in tf1.paragraphs[1:]:
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_MUTED
        p.space_after = Pt(2)

    add_card(s11, Inches(4.8), Inches(2.0), Inches(3.7), Inches(4.7))
    tb2 = s11.shapes.add_textbox(Inches(4.95), Inches(2.15), Inches(3.4), Inches(4.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    p.text = "UNIT ECONOMICS & COST ADVANTAGE"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_EMERALD
    p.space_after = Pt(6)
    tf2.add_paragraph().text = "Node Hardware Bill of Materials (BOM):"
    tf2.add_paragraph().text = "• ESP32 MCU + Sensor Interface: LKR 3,200"
    tf2.add_paragraph().text = "• Tipping Bucket Rain Gauge: LKR 4,800"
    tf2.add_paragraph().text = "• Solar Panel (5W) + TP4056 + Battery: LKR 3,500"
    tf2.add_paragraph().text = "• SIM800L / Enclosure / Mounting: LKR 3,000"
    tf2.add_paragraph().text = "• Total Per-Node CapEx: ~LKR 14,500 ($48 USD)"
    tf2.add_paragraph().text = "\nMarket Disruption Benchmark:"
    tf2.add_paragraph().text = "• Imported Commercial Stations (OTT / Campbell Scientific): LKR 380,000 – 500,000 ($1,500 USD)."
    tf2.add_paragraph().text = "• Cost Advantage: 26x Cheaper! Allows dense spatial deployment across entire river reaches."
    for p in tf2.paragraphs[1:]:
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_WHITE if "26x Cheaper" in p.text or "Total" in p.text else C_MUTED
        p.space_after = Pt(2)

    add_card(s11, Inches(8.8), Inches(2.0), Inches(3.7), Inches(4.7))
    tb3 = s11.shapes.add_textbox(Inches(8.95), Inches(2.15), Inches(3.4), Inches(4.4))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p = tf3.paragraphs[0]
    p.text = "3-YEAR FINANCIAL PROJECTIONS"
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = C_AMBER
    p.space_after = Pt(6)
    tf3.add_paragraph().text = "Pilot Phase (Year 1 - 50 Nodes):"
    tf3.add_paragraph().text = "• CapEx: LKR 725,000 | OpEx: LKR 450,000"
    tf3.add_paragraph().text = "• Projected Revenue: LKR 2.2M (B2G Pilot + Grant)"
    tf3.add_paragraph().text = "• Year 1 ROI: ~87.5% (Break-even in Month 8)"
    tf3.add_paragraph().text = "\nGrowth Phase (Year 2 - 150 Nodes):"
    tf3.add_paragraph().text = "• Annual Revenue: LKR 5.8M | Net Margin: 48%"
    tf3.add_paragraph().text = "• Onboard 2 major agricultural/insurance clients."
    tf3.add_paragraph().text = "\nScale Phase (Year 3 - 450 Nodes National):"
    tf3.add_paragraph().text = "• Annual Revenue: LKR 14.5M | Net Margin: 56%"
    tf3.add_paragraph().text = "• Multilateral donor funding (World Bank / ADB Climate Resilience Facility)."
    for p in tf3.paragraphs[1:]:
        p.font.name = "Arial"
        p.font.size = Pt(9.5)
        p.font.color.rgb = C_WHITE if "ROI" in p.text else C_MUTED
        p.space_after = Pt(2)

    add_footer(s11, 11)

    # ==========================================================================
    # SLIDE 12: ROADMAP & SUSTAINABILITY
    # ==========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Deployment Roadmap & Social Impact", "Phased National Rollout Plan & Sustainable Community Resilience", "From Kelani river basin pilot to a nationwide disaster early warning network protecting 11M+ citizens")

    phases = [
        ("PHASE 1: PILOT DEPLOYMENT (YEAR 0–1)", [
            "• Deploy 50 solar IoT nodes across high-risk Kelani reaches (Sedawatta, Hanwella, Kaduwela).",
            "• Integrate with Disaster Management Centre (DMC) emergency operations room.",
            "• Validate live ML model accuracy against actual 2026/2027 monsoon events.",
            "• Target Beneficiaries: 500,000 vulnerable riverine citizens in Western Province."
        ], C_CYAN),
        ("PHASE 2: BASIN-WIDE EXPANSION (YEAR 2)", [
            "• Expand network to 150 nodes covering the entire Kelani Ganga catchment.",
            "• Deploy localized village siren controllers in flood-prone Grama Niladhari divisions.",
            "• Onboard parametric insurance partners for automated agricultural crop loss payouts.",
            "• Train local youth technicians for routine hardware maintenance."
        ], C_WATER_BLUE),
        ("PHASE 3: NATIONAL SCALE (YEAR 3–5)", [
            "• Replicate architecture across other disaster-prone river basins (Kalu Ganga, Gin Ganga, Nilwala Ganga).",
            "• Total Network: 450+ autonomous solar IoT nodes covering 11 Million people.",
            "• Partner with UNDP, World Bank Climate Adaptation Fund, and Asian Development Bank (ADB).",
            "• Social Mission: 100% free SMS warnings for registered low-income households."
        ], C_EMERALD)
    ]
    for idx, (p_title, p_items, col) in enumerate(phases):
        cx = Inches(0.8 + idx * 2.98)
        add_card(s12, cx, Inches(2.0), Inches(2.8), Inches(4.7))
        tb = s12.shapes.add_textbox(cx + Inches(0.15), Inches(2.15), Inches(2.5), Inches(4.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p1 = tf.paragraphs[0]
        p1.text = p_title
        p1.font.name = "Arial"
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = col
        p1.space_after = Pt(10)
        for it in p_items:
            p = tf.add_paragraph()
            p.text = it
            p.font.name = "Arial"
            p.font.size = Pt(10)
            p.font.color.rgb = C_MUTED
            p.space_after = Pt(6)

    add_footer(s12, 12)

    # ==========================================================================
    # SLIDE 13: CONCLUSION
    # ==========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Conclusion & Transition to Demonstration", "Key Research Contributions & Live Demonstration Sequence", "Transforming theoretical machine learning into an actionable, life-saving early warning system")

    add_card(s13, Inches(0.8), Inches(2.0), Inches(5.7), Inches(4.7))
    tb_c = s13.shapes.add_textbox(Inches(1.0), Inches(2.15), Inches(5.3), Inches(4.4))
    tfc = tb_c.text_frame
    tfc.word_wrap = True
    p = tfc.paragraphs[0]
    p.text = "RESEARCH CONTRIBUTIONS & VALUE DELIVERED"
    p.font.name = "Arial"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = C_CYAN
    p.space_after = Pt(8)
    tfc.add_paragraph().text = "1. Micro-Catchment Spatial Disruption: Solved the 25km synoptic forecasting resolution blind-spot using sub-kilometer calibrated edge IoT sensing."
    tfc.add_paragraph().text = "2. Multi-Horizon Predictive ML: Engineered a LightGBM multi-output framework projecting 24h, 48h, and 72h rainfall depths (R² = 0.841, MAE = 2.84mm)."
    tfc.add_paragraph().text = "3. Two-Stage Inundation Intelligence: Deployed Distance-Based Dynamic Flood Risk (DFRS) evaluating occurrence, risk score, arrival time, and water depth."
    tfc.add_paragraph().text = "4. 26x Cost Innovation & Commercial Feasibility: Low-cost LKR 14,500 solar nodes provide a financially sustainable, scalable business model for DMC and insurers."
    tfc.add_paragraph().text = "5. Humanitarian Impact: Trilingual community alerting directly reduces evacuation response times, protecting lives and livelihoods."
    for p in tfc.paragraphs[1:]:
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.color.rgb = C_MUTED
        p.space_after = Pt(4)

    add_card(s13, Inches(6.8), Inches(2.0), Inches(5.7), Inches(4.7), bg_rgb=RGBColor(26, 43, 76), border_rgb=C_CYAN)
    tb_d = s13.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.3))
    tfd = tb_d.text_frame
    tfd.word_wrap = True
    p = tfd.paragraphs[0]
    p.text = "LIVE TECHNICAL DEMONSTRATION"
    p.font.name = "Arial"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = C_WHITE
    p.space_after = Pt(10)
    tfd.add_paragraph().text = "We invite the examination committee to observe the 10-minute live demonstration:"
    tfd.add_paragraph().text = "1. Live IoT Telemetry: ESP32 node publishing real-time tipping pulses over HiveMQ Cloud Broker."
    tfd.add_paragraph().text = "2. AI Weather Fusion: FastAPI backend ingesting live Open-Meteo atmospheric variables."
    tfd.add_paragraph().text = "3. Multi-Horizon Dashboard: Streamlit AI interface displaying 24h, 48h, 72h predictive curves."
    tfd.add_paragraph().text = "4. Severe Storm Simulation: Injecting 250mm monsoonal burst into the live inference pipeline."
    tfd.add_paragraph().text = "5. End-to-End React UI Sync: Executing Two-Stage XGBoost model live in the browser."
    tfd.add_paragraph().text = "\nThank you. We are ready to begin the demonstration."
    for p in tfd.paragraphs[1:]:
        p.font.name = "Arial"
        p.font.size = Pt(10)
        p.font.color.rgb = C_LIGHT_BLUE if "Thank you" in p.text else C_MUTED
        p.space_after = Pt(3)

    add_footer(s13, 13)

    prs.save(output_pptx)
    print(f"[OK] Successfully saved PPTX: {output_pptx}")


# ==============================================================================
# REPORTLAB PDF VERSION (All 13 Slides in 16:9 Landscape)
# ==============================================================================
def create_unified_pdf(output_pdf="SLIIT_R26_IT_162_Final_Presentation.pdf"):
    print(f"[*] Building 16:9 Landscape Presentation PDF (All 13 Slides): {output_pdf}")
    page_w, page_h = 792, 445.5 # 16:9 widescreen points
    
    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=(page_w, page_h),
        leftMargin=30,
        rightMargin=30,
        topMargin=25,
        bottomMargin=25
    )

    styles = getSampleStyleSheet()
    story = []

    p_title = ParagraphStyle('PDF_Title', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=colors.HexColor("#0f172a"), spaceAfter=3)
    p_sub = ParagraphStyle('PDF_Sub', parent=styles['Normal'], fontName='Helvetica', fontSize=9.5, leading=12, textColor=colors.HexColor("#0284c7"), spaceAfter=8)
    p_head = ParagraphStyle('PDF_Head', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=9.5, leading=12, textColor=colors.HexColor("#1e3a8a"))
    p_body = ParagraphStyle('PDF_Body', parent=styles['Normal'], fontName='Helvetica', fontSize=7.6, leading=10, textColor=colors.HexColor("#334155"))

    def make_slide(tag, title, sub, col1_title, col1_items, col2_title, col2_items, col3_title=None, col3_items=None):
        elems = []
        elems.append(Paragraph(f"<b>{tag.upper()}</b>", ParagraphStyle('Tag', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=7.5, leading=9, textColor=colors.HexColor("#0284c7"))))
        elems.append(Paragraph(title, p_title))
        if sub:
            elems.append(Paragraph(sub, p_sub))
        
        c1 = [Paragraph(f"<b>{col1_title}</b>", p_head), Spacer(1, 3)]
        for it in col1_items:
            c1.append(Paragraph(f"• {it}", p_body))
            c1.append(Spacer(1, 1.5))

        c2 = [Paragraph(f"<b>{col2_title}</b>", p_head), Spacer(1, 3)]
        for it in col2_items:
            c2.append(Paragraph(f"• {it}", p_body))
            c2.append(Spacer(1, 1.5))

        if col3_title and col3_items:
            c3 = [Paragraph(f"<b>{col3_title}</b>", p_head), Spacer(1, 3)]
            for it in col3_items:
                c3.append(Paragraph(f"• {it}", p_body))
                c3.append(Spacer(1, 1.5))
            t = Table([[c1, c2, c3]], colWidths=[240, 240, 240])
        else:
            t = Table([[c1, c2]], colWidths=[360, 360])

        t.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
            ('TOPPADDING', (0,0), (-1,-1), 6),
            ('BOTTOMPADDING', (0,0), (-1,-1), 6),
            ('LEFTPADDING', (0,0), (-1,-1), 8),
            ('RIGHTPADDING', (0,0), (-1,-1), 8),
        ]))
        elems.append(t)
        elems.append(Spacer(1, 8))
        elems.append(Paragraph("<font size='7' color='#94a3b8'>SLIIT CDAP R26-IT-162 | FloodSense AI | Final Year Comprehensive Viva Defense Presentation</font>", styles['Normal']))
        elems.append(PageBreak())
        return elems

    # Slide 1: Title
    story.append(Paragraph("<b>SLIIT FACULTY OF COMPUTING | CDAP RESEARCH DEFENSE R26-IT-162</b>", p_sub))
    story.append(Paragraph("FloodSense AI: Intelligent IoT Microclimate Sensing & Dual-Stage Predictive Flood Inundation Modeling", p_title))
    story.append(Paragraph("Hyperlocal Rainfall Forecasting & Distance-Based Dynamic Risk Scoring for Kelani River Basin Communities", p_sub))
    story.append(Spacer(1, 10))

    t_team = Table([[
        [
            Paragraph("<b>STUDENT A (IT21313998)</b>", p_head),
            Paragraph("<b>Rasara S.H.K.</b> — Embedded IoT & Rainfall ML", p_sub),
            Paragraph("• ESP32 calibrated tipping bucket rain gauge node (0.2mm per tip)", p_body),
            Paragraph("• HiveMQ Cloud MQTT broker & non-blocking signal processing", p_body),
            Paragraph("• Open-Meteo 14-variable atmospheric live data fusion engine", p_body),
            Paragraph("• LightGBM/XGBoost multi-horizon rainfall forecasting (24h, 48h, 72h)", p_body),
        ],
        [
            Paragraph("<b>STUDENT B (IT22236814)</b>", p_head),
            Paragraph("<b>U.H.K. Sankalana</b> — Flood Risk & SaaS Dashboard", p_sub),
            Paragraph("• Distance-Based Dynamic Flood Risk Personalization (DFRS)", p_body),
            Paragraph("• Stage 1A: XGBoost Binary Occurrence Classifier (F1 = 0.941)", p_body),
            Paragraph("• Stage 1B: XGBoost Continuous Risk Regressor (0–100 Scale)", p_body),
            Paragraph("• Stage 2: Multi-Output Regressor (Arrival Time hrs & Water Height m)", p_body),
            Paragraph("• React SaaS Dashboard with Sinhala, Tamil & English alerts", p_body),
        ]
    ]], colWidths=[360, 360])
    t_team.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f1f5f9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#cbd5e1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_team)
    story.append(PageBreak())

    # Slide 2: Problem
    story.extend(make_slide(
        "Problem Context & Socio-Economic Impact", "The Kelani River Basin Flood Crisis & Early Warning Deficit", "500,000+ vulnerable citizens face severe recurring disaster across Colombo, Gampaha & Kegalle",
        "Current Systemic Deficits", ["Coarse 25 km synoptic grids miss micro-catchment cloudbursts.", "Manual gauge reporting collects water levels once every 6–12 hours.", "Binary blanket alerts lack doorstep personalization.", "No inundation arrival time or localized water depth forecasting."],
        "Humanitarian & Economic Cost", ["LKR 50+ Billion in direct annual economic losses.", "300,000+ people displaced annually in urban lower reaches.", "50–100+ fatalities in catastrophic monsoon events (2016, 2021).", "15–30 days of recurring transport and business disruption."]
    ))

    # Slide 3: Evolution
    story.extend(make_slide(
        "Reviewer Feedback & System Evolution", "How We Addressed Reviewer Comments & Upgraded the Research", "Systematic progression from a basic monitoring prototype to an enterprise-grade AI flood early warning system",
        "Sensor & Pipeline Evolution", ["From: Single sensor monitoring ➔ To: Multi-factor IoT array (Tipping bucket, reed switch debouncing ISR, Open-Meteo fusion).", "From: Manual logs & once-a-day polling ➔ To: Sub-second MQTT streaming via HiveMQ Cloud Broker."],
        "AI Modeling & Alerting Evolution", ["From: Binary flood alerts (Yes/No) ➔ To: Dual-stage ML pipeline providing continuous risk score (0-100), arrival time, and depth.", "From: Generic text notifications ➔ To: Personalized Distance-Based Dynamic Risk (DFRS) in Sinhala, Tamil, English."]
    ))

    # Slide 4: Architecture
    story.extend(make_slide(
        "System Architecture & Data Flow", "The Integrated Symbiotic Pipeline: Sensor to Inundation Decision", "Seamless cross-tier data pipeline connecting Student A's IoT & ML engine with Student B's flood risk models",
        "Component A: Sensing & Rain ML", ["ESP32 Microcontroller with interrupt-driven tipping bucket.", "HiveMQ Cloud MQTT Broker (sub-second telemetry ingestion).", "Open-Meteo live atmospheric fusion (14 variables).", "LightGBM multi-horizon predictor for 24h, 48h, and 72h rainfall."],
        "Component B: Two-Stage Flood ML & UI", ["Stage 1A XGBoost Binary Classifier (Occurrence Yes/No).", "Stage 1B XGBoost Regressor (Continuous Risk Score 0–100).", "Stage 2 Multi-Output Regressor (Arrival Time & Water Height).", "Vite React Dashboard with trilingual emergency SOP notifications."]
    ))

    # Slide 5: Student A IoT
    story.extend(make_slide(
        "Component A | Rasara S.H.K. (IT21313998)", "Embedded IoT Microclimate Sensing & Edge Telemetry Firmware", "High-frequency rainfall pulse detection with hardware debouncing and resilient cloud messaging",
        "Hardware Architecture", ["ESP32 dual-core Xtensa 32-bit LX6 running at 240 MHz.", "Tipping bucket rain collector (calibrated at 0.20 mm per tip).", "DHT22 / BME280 temperature and relative humidity monitoring.", "Solar-powered off-grid subsystem (3.7V Li-ion + 5W solar + TP4056)."],
        "Signal Processing & MQTT", ["Interrupt Service Routine (ISR) executed in high-speed IRAM.", "100 ms software debounce lock eliminating reed contact chatter.", "Median filter rejecting false positive spikes from wind-blown debris.", "Lightweight MQTT v3.1.1 telemetry over HiveMQ Cloud Broker."]
    ))

    # Slide 6: Student A ML
    story.extend(make_slide(
        "Component A | Rasara S.H.K. (IT21313998)", "Multi-Horizon Machine Learning Rainfall Forecasting Engine", "Coupling atmospheric reanalysis with edge telemetry to predict 24h, 48h, and 72h precipitation depths",
        "Data Fusion & Feature Pipeline", ["14 Open-Meteo variables (CAPE, 2m temp, surface pressure, RH, cloud).", "Orthogonal wind vector decomposition: u = -s·sin(θ) and v = -s·cos(θ).", "Rolling antecedent windows (1h, 3h, 6h, 12h, 24h, 48h, 72h, 7-day).", "Antecedent Precipitation Index (API) with recession constant k = 0.88."],
        "Model Benchmarks & Results", ["🏆 LightGBM Regressor: R² = 0.841 | MAE = 2.84 mm | RMSE = 4.12 mm.", "🥈 XGBoost Regressor: R² = 0.835 | MAE = 2.98 mm | RMSE = 4.25 mm.", "Rain Occurrence Classifier: F1-score = 0.912 and ROC-AUC = 0.945.", "Zero lookahead bias enforced via TimeSeriesSplit cross-validation."]
    ))

    # Slide 7: Student B Models
    story.extend(make_slide(
        "Component B | U.H.K. Sankalana (IT22236814)", "Two-Stage Machine Learning Dynamic Flood Risk & Inundation Model", "Combining hydro-topographic vectors with rainfall predictions to compute occurrence, risk score, arrival time, and depth",
        "Stage 1A & 1B Models", ["Stage 1A: XGBoost Classifier (F1 = 0.941) evaluates Flood Occurrence.", "Bayesian posterior probability calibrated against 10-year Kelani records.", "Stage 1B: XGBoost Regressor (RMSE = 3.12) calculates 0–100 Risk Score.", "Categorized into Low (<30), Moderate (30–49), High (50–69), Very High (≥70)."],
        "Stage 2 Multi-Output Model", ["Executes conditionally when Stage 1A predicts Flood Occurrence = Yes.", "Metric 1: Inundation Arrival Time (hours until wavefront reaches community).", "Metric 2: Peak Inundation Height (water depth in meters above ground).", "Integrates distance to river, terrain elevation, and soil classification."]
    ))

    # Slide 8: Student B UI
    story.extend(make_slide(
        "Component B | U.H.K. Sankalana (IT22236814)", "Distance-Based Dynamic Flood Risk Personalization (DFRS)", "Hyperlocal spatial proximity modeling, executive React dashboard UI, and trilingual community alerts",
        "Distance-Based Personalization", ["Proximity decay algorithm scales risk as river channel distance decreases.", "Couples digital elevation (DEM/SRTM), soil type (Clay), and land cover.", "Sedawatta (45m river distance, 3.2m elevation) ➔ High Risk (Arrival 3.4h, Height 3.84m).", "Malabe (1,250m river distance, 32m elevation) ➔ Safe baseline."],
        "Executive React Dashboard", ["Tailwind CSS with SVG semi-circular risk dials and model KPI banners.", "Live API health check indicator monitoring Flask backend on port 5000.", "1-Click Viva Demonstration Presets (Sedawatta, Ja-Ela, Malabe).", "Trilingual notification dispatch in Sinhala, Tamil, and English."]
    ))

    # Slide 9: Integration
    story.extend(make_slide(
        "Cross-System Integration & Data Contract", "How Component A Feeds Component B in Real-Time", "The automated mapping pipeline transforming multi-horizon rainfall forecasts into the 12-feature flood matrix",
        "Component A Handoff Payload", ["rainfall_7d_mm: Cumulative antecedent precipitation (e.g. 200 mm).", "monthly_rainfall_mm: 30-day baseline catchment saturation (e.g. 350 mm).", "rainfall_intensity_mmhr: Peak storm cloudburst intensity (e.g. 15–28 mm/hr).", "Exposed via automated REST API (/api/v1/forecast/latest) and in-process bridge."],
        "Component B Execution Result", ["Binds Component A's rainfall with 9 geospatial features (lat/lon, elevation, soil).", "Clicking '⚡ Sync IoT Rainfall' in React UI executes live prediction.", "Yields: Occurrence = YES, Risk = 56.92%, Arrival = 3.41h, Water Height = 3.84m.", "Demonstrates genuine end-to-end multi-disciplinary research cohesion."]
    ))

    # Slide 10: Testing
    story.extend(make_slide(
        "Empirical Validation & Community Field Trials", "Field Testing Across Kelani Riverine Communities & Post-Test Iterations", "Tested over 3 weeks across 3 agricultural riverine locations capturing 12 real monsoon rainfall events",
        "Field Trial Protocol & Scores", ["Tested across Sedawatta (Lower Reach), Hanwella, and Kaduwela.", "15 riverine households, 5 farmers, and 2 disaster coordinators participated.", "Overall user satisfaction rating: 4.4 / 5.0.", "Alert timeliness: 4.6 / 5.0 (average 4.2 hours actionable evacuation lead time)."],
        "Post-Testing Iterations Implemented", ["Added 5-sample median filtering in firmware to prevent false tips from debris.", "Configurable distance weighting added to DFRS personalization algorithm.", "Optimized deep-sleep power cycling, extending off-grid battery life to 90 days.", "Automated SMS receipt acknowledgement added for emergency coordinators."]
    ))

    # Slide 11: Commercialization
    story.extend(make_slide(
        "Commercialization & Market Feasibility", "Business Model, Unit Economics & 3-Year Financial Sustainability", "A high-margin, scalable B2G & B2B SaaS model providing 26x cost disruption over imported stations",
        "Multi-Stream Revenue Model", ["B2G Municipal Contracts: Annual monitoring SLA with Disaster Management Centre (DMC) & Irrigation Dept (LKR 1.5M - 2.5M/yr).", "Insurance Data-as-a-Service (DaaS): Parametric flood risk verification API for insurers (Ceylinco, Sri Lanka Insurance) at LKR 250k/mo.", "B2B Commercial Agriculture: Real-time microclimate soil-moisture feeds for tea/rubber estates in upstream catchment reaches."],
        "Unit Economics & Projections", ["Per-Node CapEx: ~LKR 14,500 ($48 USD) vs Imported Stations LKR 400,000+ (26x Cheaper!).", "Pilot Phase (Year 1 - 50 Nodes): CapEx LKR 725k, Break-even in Month 8, Year 1 ROI ~87.5%.", "Growth Phase (Year 2 - 150 Nodes): Revenue LKR 5.8M with 48% net margin.", "Scale Phase (Year 3 - 450 Nodes National): Revenue LKR 14.5M across 4 major river basins."]
    ))

    # Slide 12: Roadmap
    story.extend(make_slide(
        "Deployment Roadmap & Social Impact", "Phased National Rollout Plan & Sustainable Community Resilience", "From Kelani river basin pilot to a nationwide disaster early warning network protecting 11M+ citizens",
        "Phased Rollout Strategy", ["Phase 1 (Year 0–1): 50-node Kelani Basin pilot, DMC integration, 500,000 people protected.", "Phase 2 (Year 2): Scale to 150 nodes covering entire Kelani basin; onboard insurance partners.", "Phase 3 (Year 3–5): National rollout to Kalu Ganga, Gin Ganga, and Nilwala basins (450+ nodes)."],
        "Social Mission & Sustainability", ["100% free SMS warnings for registered low-income riverine households.", "Solar-powered off-grid hardware with local youth technician maintenance training.", "Supports UN Sustainable Development Goals (SDG 11: Sustainable Cities, SDG 13: Climate Action).", "Partnership pathways with World Bank and Asian Development Bank Climate Facilities."]
    ))

    # Slide 13: Conclusion
    story.extend(make_slide(
        "Conclusion & Transition to Demonstration", "Key Research Contributions & Live Demonstration Sequence", "Transforming theoretical machine learning into an actionable, life-saving early warning system",
        "Research Contributions", ["Sub-kilometer spatial disruption solving the 25km synoptic forecasting blind-spot.", "Multi-horizon LightGBM predictive framework (R² = 0.841, MAE = 2.84 mm).", "Two-Stage Inundation Intelligence predicting arrival time and water depth.", "26x cost innovation proving sustainable commercial viability for Sri Lanka."],
        "Live Demonstration Sequence", ["1. Live IoT Telemetry: ESP32 node streaming pulses to HiveMQ Cloud.", "2. AI Weather Fusion: FastAPI backend fetching live Open-Meteo grids.", "3. AI Forecast Dashboard: Streamlit multi-horizon predictive curves.", "4. Storm Simulation Mode: Injecting 250mm cloudburst scenario.", "5. End-to-End React UI Sync: Executing Two-Stage XGBoost model live."]
    ))

    doc.build(story)
    print(f"[OK] Successfully saved Landscape PDF: {output_pdf}")


if __name__ == "__main__":
    out_pptx = "SLIIT_R26_IT_162_Final_Presentation.pptx"
    out_pdf  = "SLIIT_R26_IT_162_Final_Presentation.pdf"
    create_unified_pptx(out_pptx)
    create_unified_pdf(out_pdf)
