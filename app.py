import base64
import hashlib
import json
import sqlite3
from datetime import datetime
from pathlib import Path

import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

st.set_page_config(page_title="ArtLink - Where Creativity Meets Opportunity", layout="wide", initial_sidebar_state="collapsed")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&family=Inter:wght@400;500;600;700;800&display=swap');

:root{
    --bg-0:#efe8db;
    --bg-1:#e6dac9;
    --bg-2:#d9d0c1;
    --bg-3:#cfd8d1;
    --card: rgba(252,246,236,0.92);
    --card-light: rgba(249,241,229,0.84);
    --border: rgba(15,23,42,0.08);
    --border-light: rgba(15,23,42,0.12);
    --accent-a:#17324d;
    --accent-b:#2a9d8f;
    --accent-c:#334155;
    --accent-d:#b08968;
    --text:#0f172a;
    --text-muted:#475569;
    --muted:#64748b;
}

.stApp{
    background:
        radial-gradient(1000px circle at 18% 12%, rgba(23,50,77,0.10), transparent 56%),
        radial-gradient(900px circle at 84% 16%, rgba(42,157,143,0.09), transparent 52%),
        radial-gradient(850px circle at 52% 96%, rgba(176,137,104,0.08), transparent 60%),
        linear-gradient(180deg,var(--bg-0) 0%,var(--bg-1) 40%,var(--bg-2) 70%,var(--bg-3) 100%);
    color: var(--text);
    font-family: 'Poppins', 'Inter', sans-serif;
    background-attachment: fixed;
    overflow-x: hidden;
}
.block-container{
    max-width: 1400px;
    padding-top: 3rem;
    padding-left: 2rem;
    padding-right: 2rem;
    animation: fadeInUp .8s ease;
}
.block-container::after{
    content:"";
    position: fixed;
    inset: 0;
    pointer-events: none;
    background-image: url("data:image/svg+xml,%3Csvg width='120' height='120' viewBox='0 0 120 120' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='2' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='120' height='120' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
    mix-blend-mode: soft-light;
}

[data-testid="stAlert"]{
    border-radius: 12px;
    border: 1px solid rgba(180, 83, 9, 0.30);
    background: linear-gradient(135deg, rgba(255, 247, 223, 0.96), rgba(245, 230, 186, 0.92));
}
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p,
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] li,
[data-testid="stAlert"] [data-testid="stMarkdownContainer"] span{
    color: #3f2a0d !important;
    font-weight: 600;
}

.hero{
    position: relative;
    padding: 60px 50px;
    border-radius: 28px;
    background: linear-gradient(135deg, rgba(252,246,236,0.98) 0%, rgba(247,238,224,0.95) 52%, rgba(240,233,221,0.94) 100%);
    border: 1px solid var(--border-light);
    box-shadow: 0 26px 50px rgba(15,23,42,0.10), inset 0 1px 0 rgba(255,255,255,0.75);
    overflow: hidden;
    backdrop-filter: blur(20px);
}
.hero::before{
    content:"";
    position:absolute;
    top:-50%;
    left:5%;
    width: 90%;
    height: 200%;
    background: linear-gradient(90deg, rgba(23,50,77,0.10), rgba(42,157,143,0.10), rgba(176,137,104,0.08), rgba(23,50,77,0.08));
    filter: blur(100px);
    opacity: 0.40;
    animation: glowShift 15s ease-in-out infinite;
}
@keyframes glowShift{
    0%{ transform: translateX(-15%) translateY(0%); }
    50%{ transform: translateX(15%) translateY(5%); }
    100%{ transform: translateX(-15%) translateY(0%); }
}
.hero h1{
    font-size: 52px;
    font-weight: 900;
    color: var(--text);
    letter-spacing: -0.03em;
    margin-bottom: 16px;
    background: linear-gradient(135deg, var(--text) 0%, var(--accent-b) 42%, var(--accent-a) 74%, var(--accent-d) 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: gradientShift 8s ease infinite;
}
@keyframes gradientShift{
    0%{ background-position: 0% 50%; }
    50%{ background-position: 100% 50%; }
    100%{ background-position: 0% 50%; }
}
.hero p{
    color: var(--text-muted);
    font-size: 18px;
    line-height: 1.7;
    margin-bottom: 28px;
    max-width: 600px;
}
.hero-kpis{
    display: flex;
    flex-wrap: wrap;
    gap: 12px;
    margin-top: 10px;
}
.kpi-chip{
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 9px 14px;
    border-radius: 999px;
    border: 1px solid rgba(148,163,184,0.3);
    background: rgba(249,241,229,0.96);
    font-size: 13px;
    color: var(--text-muted);
    backdrop-filter: blur(8px);
}
.kpi-chip strong{
    color: var(--text);
}
.hero-actions{
    display: flex;
    gap: 16px;
    flex-wrap: wrap;
    margin-top: 24px;
}
.hero-panel{
    position: relative;
    padding: 24px;
    border-radius: 24px;
    background: linear-gradient(160deg, rgba(252,246,236,0.98), rgba(244,235,223,0.94));
    border: 1px solid rgba(148,163,184,0.18);
    box-shadow: 0 24px 60px rgba(15,23,42,0.10);
    overflow: hidden;
}
.hero-panel::before{
    content:"";
    position:absolute;
    inset:-20% auto auto -15%;
    width:200px;
    height:200px;
    border-radius:50%;
    background: radial-gradient(circle, rgba(176,137,104,0.18), transparent 65%);
}
.hero-panel img{
    position: relative;
    z-index: 1;
}
.hero-metrics{
    display:grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 14px;
    margin-top: 18px;
}
.hero-metric{
    padding: 16px 18px;
    border-radius: 18px;
    background: rgba(252,246,236,0.98);
    border: 1px solid rgba(148,163,184,0.18);
}
.hero-metric strong{
    display:block;
    font-size: 22px;
    color: var(--text);
}
.hero-metric span{
    color: var(--text-muted);
    font-size: 13px;
}
.home-visual-card{
    position: relative;
    padding: 18px;
    border-radius: 26px;
    background: linear-gradient(160deg, rgba(252,246,236,0.98), rgba(247,238,224,0.94));
    border: 1px solid rgba(148,163,184,0.18);
    box-shadow: 0 26px 64px rgba(15,23,42,0.10);
    overflow: hidden;
}
.home-visual-card::before{
    content:"";
    position: absolute;
    inset: -18% auto auto 55%;
    width: 220px;
    height: 220px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(42,157,143,0.14), transparent 70%);
}
.home-logo-stage{
    position: relative;
    z-index: 1;
    background: linear-gradient(180deg, rgba(252,246,236,1), rgba(247,238,224,0.98));
    border-radius: 20px;
    padding: 18px;
    box-shadow: 0 20px 40px rgba(15,23,42,0.22);
}
.home-logo-stage img{
    display: block;
    width: 100%;
    border-radius: 14px;
}
.home-metrics-grid{
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 14px;
    margin-top: 16px;
}
.feature-band{
    display:grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 18px;
    margin: 10px 0 8px;
}
.feature-tile{
    position: relative;
    padding: 22px 22px 20px;
    border-radius: 22px;
    background: linear-gradient(160deg, rgba(252,246,236,0.96), rgba(247,238,224,0.93));
    border: 1px solid rgba(148,163,184,0.18);
    box-shadow: 0 16px 40px rgba(15,23,42,0.08);
    overflow: hidden;
}
.feature-tile::after{
    content:"";
    position:absolute;
    right:-40px;
    top:-40px;
    width:120px;
    height:120px;
    border-radius:50%;
    background: radial-gradient(circle, rgba(6,182,212,0.16), transparent 70%);
}
.feature-tile strong{
    display:block;
    position: relative;
    z-index: 1;
    color: var(--text);
    font-size: 18px;
    margin-bottom: 8px;
}
.feature-tile p{
    position: relative;
    z-index: 1;
    color: var(--text-muted);
    font-size: 14px;
    line-height: 1.7;
    margin: 0;
}
.section-shell{
    padding: 26px 28px;
    border-radius: 26px;
    background: linear-gradient(150deg, rgba(16,24,48,0.84), rgba(22,31,65,0.52));
    border: 1px solid rgba(148,163,184,0.16);
    box-shadow: 0 22px 55px rgba(2,6,23,0.48);
    margin-bottom: 22px;
}
.story-card{
    padding: 26px 28px;
    border-radius: 24px;
    background: linear-gradient(145deg, rgba(19,28,57,0.88), rgba(37,50,98,0.48));
    border: 1px solid rgba(148,163,184,0.16);
    box-shadow: 0 20px 50px rgba(2,6,23,0.5);
}
.story-card h3{
    margin: 10px 0 12px;
    font-size: 26px;
    line-height: 1.2;
    color: var(--text);
}
.story-card p{
    color: var(--text-muted);
    line-height: 1.8;
    font-size: 15px;
}
.artist-grid{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 18px;
}
.artist-spotlight{
    position: relative;
    padding: 22px;
    border-radius: 22px;
    background: linear-gradient(160deg, rgba(252,246,236,0.97), rgba(247,238,224,0.93));
    border: 1px solid rgba(148,163,184,0.18);
    box-shadow: 0 18px 42px rgba(15,23,42,0.10);
    overflow: hidden;
    min-height: 100%;
}
.artist-spotlight::before{
    content:"";
    position:absolute;
    inset:auto -15% -22% auto;
    width:140px;
    height:140px;
    border-radius:50%;
    background: radial-gradient(circle, rgba(23,50,77,0.16), transparent 68%);
}
.artist-spotlight img{
    width: 72px;
    height: 72px;
    border-radius: 22px;
    object-fit: cover;
    margin-bottom: 16px;
    border: 1px solid rgba(255,255,255,0.12);
}
.artist-topline{
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap: 12px;
    margin-bottom: 10px;
}
.artist-role{
    color: var(--text-muted);
    font-size: 13px;
}
.artist-rating{
    display:inline-flex;
    align-items:center;
    gap: 8px;
    padding: 8px 12px;
    border-radius: 999px;
    background: rgba(241,245,249,0.95);
    border: 1px solid rgba(148,163,184,0.2);
    font-size: 13px;
    color: var(--text);
}
.artist-stats{
    display:flex;
    flex-wrap:wrap;
    gap: 10px;
    margin-top: 14px;
}
.artist-stats span{
    padding: 8px 10px;
    border-radius: 12px;
    background: rgba(249,241,229,0.96);
    color: var(--text-muted);
    font-size: 12px;
    border: 1px solid rgba(148,163,184,0.15);
}
.mini-note{
    color: var(--text-muted);
    font-size: 14px;
    line-height: 1.7;
}

.portal-grid{
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 20px;
}
@media (max-width: 900px){
    .portal-grid{ grid-template-columns: 1fr; }
}

.portal-card{
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 16px;
    padding: 28px 30px;
    border-radius: 24px;
    background: linear-gradient(135deg, rgba(252,246,236,0.98) 0%, rgba(247,238,224,0.94) 100%);
    border: 1px solid var(--border-light);
    box-shadow: 0 20px 50px rgba(15,23,42,0.10), inset 0 1px 0 rgba(255,255,255,0.60);
    transition: all .35s cubic-bezier(0.34, 1.56, 0.64, 1);
    backdrop-filter: blur(15px);
}
.portal-card:hover{
    transform: translateY(-12px) scale(1.02);
    box-shadow: 0 28px 70px rgba(29,78,216,0.16), inset 0 1px 0 rgba(255,255,255,0.60);
    border: 1px solid rgba(29,78,216,0.22);
    background: linear-gradient(135deg, rgba(250,244,233,1) 0%, rgba(242,233,220,0.98) 100%);
}
.portal-card::after{
    content: "";
    position: absolute;
    inset: auto -30% -45% auto;
    width: 180px;
    height: 180px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(42,157,143,0.18), transparent 65%);
    pointer-events: none;
}
.portal-media img{
    width: 100%;
    border-radius: 18px;
    box-shadow: 0 12px 32px rgba(23,50,77,0.14);
    transition: transform .4s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow .4s ease;
    object-fit: cover;
}
.portal-card:hover .portal-media img{ 
    transform: scale(1.08) rotate(0.5deg);
    box-shadow: 0 16px 48px rgba(23,50,77,0.20);
}
.portal-meta h3{
    color: var(--text);
    font-weight: 700;
    font-size: 18px;
    margin-bottom: 8px;
    line-height: 1.4;
}
.portal-meta p{
    color: var(--text-muted);
    font-size: 14px;
    line-height: 1.6;
}
.portal-actions{
    margin-top: 12px;
}

.scroll-row{
    display: flex;
    gap: 16px;
    overflow-x: auto;
    padding-bottom: 8px;
    scroll-snap-type: x mandatory;
}
.scroll-row .card{
    min-width: 240px;
    scroll-snap-align: start;
}
.scroll-row::-webkit-scrollbar{ height: 8px; }
.nav-blur{
    position: sticky;
    top: 0;
    z-index: 100;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    backdrop-filter: blur(15px);
    background: linear-gradient(180deg, rgba(252,246,236,0.96) 0%, rgba(244,235,223,0.92) 100%);
    border: 1px solid rgba(148,163,184,0.18);
    border-radius: 18px;
    padding: 22px 28px;
    margin-bottom: 24px;
    box-shadow: 0 12px 40px rgba(15,23,42,0.10);
    animation: slideDown .5s ease;
}
@keyframes slideDown{
    from{ transform: translateY(-20px); opacity: 0; }
    to{ transform: translateY(0); opacity: 1; }
}
.nav-title{
    font-size: 40px;
    font-weight: 800;
    color: var(--text);
    letter-spacing: -0.03em;
    line-height: 1.05;
    margin-bottom: 6px;
}
.nav-crumb{
    color: var(--muted);
    font-size: 17px;
    text-align: center;
}
.top-nav-wrap{
    margin: -6px 0 28px;
}
.top-nav-wrap [data-testid="column"]{
    justify-content: flex-start;
}
.top-nav-wrap .stButton > button{
    width: 100%;
    padding: 0.8rem 0.9rem;
    border-radius: 14px;
    font-size: 14px;
    box-shadow: 0 12px 28px rgba(23,50,77,0.14);
}
.divider{
    border-top: 1px solid rgba(148,163,184,0.16);
    margin: 22px 0;
}
.grid{
    display: grid;
    grid-template-columns: repeat(2, minmax(0,1fr));
    gap: 18px;
}
@media (max-width: 860px){
    .grid{ grid-template-columns: 1fr; }
}
.stagger > .card{
    opacity: 0;
    transform: translateY(12px);
    animation: cardIn .5s ease forwards;
}
.stagger > .card:nth-child(1){ animation-delay: .08s; }
.stagger > .card:nth-child(2){ animation-delay: .16s; }
.stagger > .card:nth-child(3){ animation-delay: .24s; }
.stagger > .card:nth-child(4){ animation-delay: .32s; }
@keyframes cardIn{
    to { opacity: 1; transform: translateY(0); }
}
@keyframes fadeInUp{
    from{ opacity:0; transform: translateY(8px); }
    to{ opacity:1; transform: translateY(0); }
}
.title{
    font-size: 48px;
    font-weight: 900;
    text-align: center;
    margin-bottom: 32px;
    color: var(--text);
    letter-spacing: -0.025em;
    background: linear-gradient(135deg, var(--text) 0%, var(--accent-b) 45%, var(--accent-a) 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.desc{
    text-align: left;
    font-size: 16px;
    line-height: 1.8;
    margin-bottom: 32px;
    color: var(--text-muted);
}
[data-testid="column"]{
    display: flex;
    flex-direction: column;
    justify-content: center;
}
.click-img img{
    border-radius: 20px;
    transition: 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    cursor: pointer;
    box-shadow: 0 18px 50px rgba(23,50,77,0.14);
}
.click-img img:hover{
    transform: scale(1.08) rotate(1.5deg);
    box-shadow: 0 22px 70px rgba(23,50,77,0.22);
}
.artist-name{
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 8px;
}
button{
    background: linear-gradient(135deg, var(--accent-a) 0%, var(--accent-c) 50%, var(--accent-b) 100%);
    background-size: 200% 200%;
    color: white !important;
    border: none;
    border-radius: 12px;
    font-size: 15px;
    font-weight: 600;
    padding: 12px 26px;
    box-shadow: 0 14px 35px rgba(23,50,77,0.18);
    transition: all .3s cubic-bezier(0.34, 1.56, 0.64, 1);
    position: relative;
    overflow: hidden;
    cursor: pointer;
}
button::before{
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: rgba(255,255,255,0.2);
    transition: left .3s ease;
}
button:hover{
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 18px 50px rgba(42,157,143,0.22);
    background-position: 100% 50%;
}
button:hover::before{
    left: 100%;
}
button:active{ 
    transform: translateY(-1px) scale(0.98);
}
label{ 
    color: var(--text) !important; 
    font-weight: 550;
    font-size: 14px;
}
.stRadio label, .stRadio, .stRadio * { 
    color: var(--text) !important; 
}
div[role="radiogroup"] label { 
    color: var(--text) !important; 
}
input[type="radio"] { 
    accent-color: var(--accent-a) !important; 
}
input, textarea, select {
    background: rgba(249,241,229,0.96) !important;
    border: 1px solid var(--border-light) !important;
    border-radius: 12px !important;
    color: var(--text) !important;
    font-family: 'Poppins', sans-serif !important;
    padding: 12px 14px !important;
    transition: all .25s ease !important;
}
input:focus, textarea:focus, select:focus {
    border-color: var(--accent-a) !important;
    box-shadow: 0 0 20px rgba(29,78,216,0.15) !important;
    background: rgba(252,246,236,1) !important;
}

.card{
    background: linear-gradient(135deg, rgba(252,246,236,0.98) 0%, rgba(247,238,224,0.94) 100%);
    color: var(--text);
    padding: 28px 32px;
    border-radius: 20px;
    border: 1px solid var(--border-light);
    box-shadow: 0 16px 40px rgba(23,50,77,0.10), inset 0 1px 0 rgba(255,255,255,0.70);
    margin-bottom: 24px;
    transition: all .35s cubic-bezier(0.34, 1.56, 0.64, 1);
    backdrop-filter: blur(12px);
}
.card:hover{
    transform: translateY(-10px) scale(1.01);
    box-shadow: 0 22px 60px rgba(42,157,143,0.14), inset 0 1px 0 rgba(255,255,255,0.70);
    border: 1px solid rgba(42,157,143,0.20);
    background: linear-gradient(135deg, rgba(248,250,252,1) 0%, rgba(238,242,247,0.96) 100%);
}
.section-wrap{
    background: linear-gradient(135deg, rgba(23,50,77,0.04) 0%, rgba(42,157,143,0.03) 100%);
    border: 1px solid var(--border-light);
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 18px;
    backdrop-filter: blur(10px);
}
.badge{
    display: inline-block;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 12px;
    color: var(--text);
    margin-right: 8px;
    background: linear-gradient(135deg, var(--text) 0%, var(--accent-b) 45%, var(--accent-a) 100%);
    backdrop-filter: blur(10px);
}
.badge-pending{ background: rgba(59, 130, 246, 0.2); color: #60a5fa; border: 1px solid rgba(59, 130, 246, 0.3); }
.badge-approved{ background: rgba(34, 197, 94, 0.2); color: #4ade80; border: 1px solid rgba(34, 197, 94, 0.3); }
.badge-rejected{ background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.3); }
.small{ 
    font-size: 13px; 
    color: var(--text-muted); 
}
.empty-state{
    background: linear-gradient(135deg, rgba(23,50,77,0.04) 0%, rgba(42,157,143,0.03) 100%);
    border: 2px dashed rgba(148,163,184,0.3);
    border-radius: 16px;
    padding: 40px 24px;
    text-align: center;
    color: var(--text-muted);
    backdrop-filter: blur(10px);
}
.stApp header{
    backdrop-filter: blur(15px);
    background: rgba(249,241,229,0.86) !important;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 10px;
}
::-webkit-scrollbar-track {
    background: transparent;
}
::-webkit-scrollbar-thumb {
    background: linear-gradient(180deg, rgba(23,50,77,0.5), rgba(42,157,143,0.3));
    border-radius: 10px;
}
::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(180deg, rgba(23,50,77,0.7), rgba(42,157,143,0.5));
}
.stat-card{
    background: linear-gradient(135deg, rgba(252,246,236,0.98) 0%, rgba(247,238,224,0.94) 100%);
    border: 1px solid var(--border-light);
    border-radius: 18px;
    padding: 20px 24px;
    text-align: center;
    box-shadow: 0 12px 32px rgba(23,50,77,0.10);
    transition: all .3s ease;
    backdrop-filter: blur(10px);
}
.stat-card:hover{
    transform: translateY(-6px);
    box-shadow: 0 16px 48px rgba(42,157,143,0.14);
    border-color: rgba(42,157,143,0.22);
}
.stat-value{
    font-size: 28px;
    font-weight: 800;
    margin-bottom: 6px;
    background: linear-gradient(135deg, var(--accent-a) 0%, var(--accent-b) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.stat-label{
    font-size: 13px;
    opacity: .85;
    color: var(--text-muted);
}
.stImage img{
    border-radius: 14px;
    box-shadow: 0 8px 20px rgba(2,6,23,0.45);
}
.live-feed{
    background: linear-gradient(135deg, rgba(252,246,236,0.96), rgba(244,235,223,0.92));
    border: 1px solid var(--border-light);
    border-radius: 18px;
    padding: 18px 20px;
    box-shadow: 0 14px 35px rgba(23,50,77,0.10);
    backdrop-filter: blur(10px);
}
.live-item{
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 15px;
    color: var(--text);
    opacity: 0;
    transform: translateY(6px);
    transition: opacity .35s ease, transform .35s ease;
}
.live-item.show{
    opacity: 1;
    transform: translateY(0);
}
.live-dot{
    width: 8px;
    height: 8px;
    border-radius: 999px;
    background: linear-gradient(90deg,var(--accent-a),var(--accent-b));
    box-shadow: 0 0 8px rgba(23,50,77,0.38);
}
.section-title{
    font-size: 32px;
    font-weight: 800;
    color: var(--text);
    margin-bottom: 12px;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, var(--text) 0%, var(--accent-b) 55%, var(--accent-a) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.section-sub{
    color: var(--text-muted);
    margin-bottom: 18px;
    font-size: 15px;
}
.brand-chip{
    display: inline-block;
    padding: 6px 12px;
    border-radius: 999px;
    border: 1px solid rgba(148,163,184,0.28);
    color: var(--text-muted);
    background: rgba(249,241,229,0.95);
    font-size: 12px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-bottom: 12px;
}
.home-panel{
    border: 1px solid var(--border-light);
    border-radius: 22px;
    padding: 18px;
    background: linear-gradient(140deg, rgba(252,246,236,0.97), rgba(247,238,224,0.94));
    box-shadow: 0 18px 50px rgba(15,23,42,0.10);
}
.portal-section-head{
    margin: 18px 0 14px;
}
.portal-section-head h2{
    margin: 0 0 6px;
    font-size: 28px;
    color: var(--text);
}
.portal-section-head p{
    margin: 0;
    color: var(--text-muted);
}
@media (max-width: 900px){
    .block-container{
        padding-left: 1rem;
        padding-right: 1rem;
    }
    .hero{
        padding: 34px 26px;
        border-radius: 22px;
    }
    .hero h1{
        font-size: 34px;
    }
    .title{
        font-size: 34px;
        text-align: left;
    }
    .desc{
        font-size: 15px;
    }
    .feature-band{
        grid-template-columns: 1fr;
    }
    .hero-metrics{
        grid-template-columns: 1fr;
    }
}
</style>
""",
    unsafe_allow_html=True,
)

conn = sqlite3.connect("artists.db", check_same_thread=False)
conn.row_factory = sqlite3.Row
c = conn.cursor()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)
USE_DUMMY_TOP_ARTISTS = True


def now_iso() -> str:
    return datetime.utcnow().isoformat()


def dummy_top_artists():
    return [
        {
            "phone": "dummy_1",
            "full_name": "Rahul Musician",
            "art": "Singer",
            "avg_rating": 4.8,
            "area": "Mumbai",
            "profile_image_path": "",
            "description": "Live singer for weddings, events, and stage shows.",
            "total_reviews": 24,
            "total_bookings": 51,
        },
        {
            "phone": "dummy_2",
            "full_name": "Sneha Dancer",
            "art": "Classical Dance",
            "avg_rating": 4.7,
            "area": "Pune",
            "profile_image_path": "",
            "description": "Classical and contemporary stage performer.",
            "total_reviews": 19,
            "total_bookings": 44,
        },
        {
            "phone": "dummy_3",
            "full_name": "Arjun Percussionist",
            "art": "Drummer",
            "avg_rating": 4.6,
            "area": "Bengaluru",
            "profile_image_path": "",
            "description": "Fusion percussion artist for live events.",
            "total_reviews": 15,
            "total_bookings": 33,
        },
    ]


def img_to_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def hash_password(password: str) -> str:
    salt = "prayogam_salt_v1"
    return hashlib.sha256(f"{salt}:{password}".encode("utf-8")).hexdigest()


def validate_phone(phone: str) -> bool:
    return phone.isdigit() and len(phone) == 10


def status_badge(status: int) -> str:
    if status == 1:
        return "<span class='badge badge-approved'>Approved</span>"
    if status == -1:
        return "<span class='badge badge-rejected'>Rejected</span>"
    return "<span class='badge badge-pending'>Pending</span>"


def save_uploaded_image(uploaded_file, prefix: str):
    if uploaded_file is None:
        return None
    filename = safe_name(f"{prefix}_{int(datetime.utcnow().timestamp())}_{uploaded_file.name}")
    file_path = UPLOAD_DIR / filename
    try:
        img = Image.open(uploaded_file).convert("RGB")
        img.thumbnail((1400, 1400))
        img.save(file_path, format="JPEG", quality=85, optimize=True)
        return str(file_path)
    except Exception:
        return None


def safe_name(name: str) -> str:
    keep = "._-"
    return "".join(ch if ch.isalnum() or ch in keep else "_" for ch in name)


def db_init():
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS artist_users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Name TEXT NOT NULL,
            Phone_Number TEXT UNIQUE NOT NULL,
            password_hash TEXT,
            created_at TEXT
        )
        """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS artist_profile(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            phone TEXT UNIQUE,
            full_name TEXT,
            art TEXT,
            description TEXT,
            area TEXT,
            drive TEXT,
            skills TEXT,
            email TEXT,
            profile_image_path TEXT,
            approval_status INTEGER DEFAULT 0,
            updated_at TEXT,
            FOREIGN KEY(phone) REFERENCES artist_users(Phone_Number)
        )
        """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS client_users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT
        )
        """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS portfolio_items(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_phone TEXT NOT NULL,
            title TEXT NOT NULL,
            image_path TEXT NOT NULL,
            created_at TEXT,
            FOREIGN KEY(artist_phone) REFERENCES artist_users(Phone_Number)
        )
        """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS portfolio_links(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_phone TEXT NOT NULL,
            platform TEXT,
            url TEXT NOT NULL,
            created_at TEXT
        )
        """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS bookings(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_phone TEXT NOT NULL,
            client_phone TEXT,
            client_name TEXT NOT NULL,
            client_email TEXT,
            message TEXT,
            event_date TEXT,
            budget REAL,
            status TEXT DEFAULT 'Pending',
            review_submitted INTEGER DEFAULT 0,
            created_at TEXT,
            FOREIGN KEY(artist_phone) REFERENCES artist_users(Phone_Number)
        )
        """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS reviews(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            artist_phone TEXT NOT NULL,
            client_phone TEXT,
            booking_id INTEGER,
            rating INTEGER CHECK(rating >= 1 AND rating <= 5),
            comment TEXT,
            created_at TEXT,
            FOREIGN KEY(artist_phone) REFERENCES artist_users(Phone_Number)
        )
        """
    )

    c.execute(
        """
        CREATE TABLE IF NOT EXISTS favorites(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_phone TEXT NOT NULL,
            artist_phone TEXT NOT NULL,
            created_at TEXT,
            UNIQUE(client_phone, artist_phone)
        )
        """
    )

    # Backward-compatible migration for older DBs.
    _safe_add_column("artist_users", "password_hash", "TEXT")
    _safe_add_column("artist_users", "created_at", "TEXT")
    _safe_add_column("artist_profile", "skills", "TEXT")
    _safe_add_column("artist_profile", "email", "TEXT")
    _safe_add_column("artist_profile", "profile_image_path", "TEXT")
    _safe_add_column("artist_profile", "approval_status", "INTEGER DEFAULT 0")
    _safe_add_column("artist_profile", "updated_at", "TEXT")
    _safe_add_column("bookings", "review_submitted", "INTEGER DEFAULT 0")
    _safe_add_column("reviews", "client_phone", "TEXT")
    _safe_add_column("reviews", "booking_id", "INTEGER")
    _safe_add_column("reviews", "artist_phone", "TEXT")
    _safe_add_column("bookings", "artist_phone", "TEXT")
    _safe_add_column("bookings", "client_phone", "TEXT")
    _safe_add_column("bookings", "client_name", "TEXT")
    _safe_add_column("bookings", "client_email", "TEXT")
    _safe_add_column("favorites", "client_phone", "TEXT")
    _safe_add_column("favorites", "artist_phone", "TEXT")
    _safe_add_column("portfolio_items", "artist_phone", "TEXT")

    migrate_legacy_schema()

    conn.commit()


def _safe_add_column(table: str, col: str, ddl: str):
    cols = {row["name"] for row in c.execute(f"PRAGMA table_info({table})").fetchall()}
    if col not in cols:
        c.execute(f"ALTER TABLE {table} ADD COLUMN {col} {ddl}")


def _table_columns(table: str):
    return {row["name"] for row in c.execute(f"PRAGMA table_info({table})").fetchall()}


def migrate_legacy_schema():
    # Reviews table compatibility: old schema used artist_user_id/reviewer_name.
    review_cols = _table_columns("reviews")
    if "artist_phone" not in review_cols:
        _safe_add_column("reviews", "artist_phone", "TEXT")
    if "client_phone" not in review_cols:
        _safe_add_column("reviews", "client_phone", "TEXT")
    if "booking_id" not in review_cols:
        _safe_add_column("reviews", "booking_id", "INTEGER")

    # Populate artist_phone for legacy rows where only artist_user_id exists.
    if "artist_user_id" in review_cols:
        c.execute(
            """
            UPDATE reviews
            SET artist_phone = (
                SELECT phone FROM users u WHERE u.id = reviews.artist_user_id
            )
            WHERE (artist_phone IS NULL OR artist_phone = '')
            """
        )

    # Bookings table compatibility: old schema used artist_user_id/requester_*.
    booking_cols = _table_columns("bookings")
    if "artist_phone" not in booking_cols:
        _safe_add_column("bookings", "artist_phone", "TEXT")
    if "client_phone" not in booking_cols:
        _safe_add_column("bookings", "client_phone", "TEXT")
    if "client_name" not in booking_cols:
        _safe_add_column("bookings", "client_name", "TEXT")
    if "client_email" not in booking_cols:
        _safe_add_column("bookings", "client_email", "TEXT")
    if "review_submitted" not in booking_cols:
        _safe_add_column("bookings", "review_submitted", "INTEGER DEFAULT 0")

    if "artist_user_id" in booking_cols:
        c.execute(
            """
            UPDATE bookings
            SET artist_phone = (
                SELECT phone FROM users u WHERE u.id = bookings.artist_user_id
            )
            WHERE (artist_phone IS NULL OR artist_phone = '')
            """
        )
    if "requester_name" in booking_cols:
        c.execute(
            "UPDATE bookings SET client_name=requester_name WHERE (client_name IS NULL OR client_name='')"
        )
    if "requester_email" in booking_cols:
        c.execute(
            "UPDATE bookings SET client_email=requester_email WHERE (client_email IS NULL OR client_email='')"
        )

    # Portfolio compatibility: old schema had user_id only.
    pcols = _table_columns("portfolio_items")
    if "artist_phone" not in pcols:
        _safe_add_column("portfolio_items", "artist_phone", "TEXT")
    if "user_id" in pcols:
        c.execute(
            """
            UPDATE portfolio_items
            SET artist_phone = (
                SELECT phone FROM users u WHERE u.id = portfolio_items.user_id
            )
            WHERE (artist_phone IS NULL OR artist_phone = '')
            """
        )

    # Favorites table compatibility: old schema used user_id/artist_user_id.
    fav_cols = _table_columns("favorites")
    if "client_phone" not in fav_cols:
        _safe_add_column("favorites", "client_phone", "TEXT")
    if "artist_phone" not in fav_cols:
        _safe_add_column("favorites", "artist_phone", "TEXT")

    if "user_id" in fav_cols:
        c.execute(
            """
            UPDATE favorites
            SET client_phone = (
                SELECT phone FROM users u WHERE u.id = favorites.user_id
            )
            WHERE (client_phone IS NULL OR client_phone = '')
            """
        )
    if "artist_user_id" in fav_cols:
        c.execute(
            """
            UPDATE favorites
            SET artist_phone = (
                SELECT phone FROM users u WHERE u.id = favorites.artist_user_id
            )
            WHERE (artist_phone IS NULL OR artist_phone = '')
            """
        )

    conn.commit()


def seed_existing_artists_passwords():
    # Existing users from old app get a default password so they can login.
    c.execute("SELECT Phone_Number FROM artist_users WHERE password_hash IS NULL OR password_hash='' ")
    rows = c.fetchall()
    for row in rows:
        c.execute(
            "UPDATE artist_users SET password_hash=?, created_at=? WHERE Phone_Number=?",
            (hash_password("artist@123"), now_iso(), row["Phone_Number"]),
        )
    conn.commit()


def bootstrap_state():
    defaults = {
        "page": "home",
        "artist_logged": False,
        "artist_phone": None,
        "client_logged": False,
        "client_phone": None,
        "admin_logged": False,
        "edit_mode": False,
        "selected_artist": None,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def rating_stats(artist_phone: str):
    row = c.execute(
        "SELECT ROUND(AVG(rating),1) AS avg_rating, COUNT(*) AS count_rating FROM reviews WHERE artist_phone=?",
        (artist_phone,),
    ).fetchone()
    avg_rating = row["avg_rating"] if row and row["avg_rating"] is not None else 0
    count_rating = row["count_rating"] if row else 0
    return avg_rating, count_rating


def artist_booking_count(artist_phone: str) -> int:
    row = c.execute("SELECT COUNT(*) AS cnt FROM bookings WHERE artist_phone=?", (artist_phone,)).fetchone()
    return int(row["cnt"] if row else 0)


def artist_recent_reviews(artist_phone: str, limit: int = 5):
    return c.execute(
        """
        SELECT rating, comment, created_at, client_phone
        FROM reviews
        WHERE artist_phone=?
        ORDER BY id DESC
        LIMIT ?
        """,
        (artist_phone, limit),
    ).fetchall()


def get_top_artists(limit: int = 6):
    if USE_DUMMY_TOP_ARTISTS:
        return dummy_top_artists()[:limit]
    try:
        rows = c.execute(
            """
            SELECT
                p.phone,
                p.full_name,
                p.art,
                p.description,
                p.area,
                p.profile_image_path,
                ROUND(COALESCE(AVG(r.rating),0),1) AS avg_rating,
                COUNT(DISTINCT r.id) AS total_reviews,
                COUNT(DISTINCT b.id) AS total_bookings
            FROM artist_profile p
            LEFT JOIN reviews r ON r.artist_phone=p.phone
            LEFT JOIN bookings b ON b.artist_phone=p.phone
            WHERE p.approval_status=1
            GROUP BY p.phone
            ORDER BY avg_rating DESC, total_bookings DESC, total_reviews DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()
        if not rows:
            return dummy_top_artists()[:limit]
        return rows
    except Exception:
        # Never break UI due to DB issues on Top Artists.
        return dummy_top_artists()[:limit]


def get_profile(artist_phone: str):
    return c.execute(
        """
        SELECT p.*, u.Name AS account_name
        FROM artist_profile p
        JOIN artist_users u ON p.phone=u.Phone_Number
        WHERE p.phone=?
        """,
        (artist_phone,),
    ).fetchone()


def get_favorite_artist_phones(client_phone: str):
    try:
        rows = c.execute(
            "SELECT artist_phone FROM favorites WHERE client_phone=?",
            (client_phone,),
        ).fetchall()
        return {row["artist_phone"] for row in rows if row["artist_phone"]}
    except sqlite3.OperationalError:
        # Legacy schema fallback: favorites(user_id, artist_user_id)
        rows = c.execute(
            """
            SELECT u.phone AS artist_phone
            FROM favorites f
            JOIN users cu ON cu.id=f.user_id
            JOIN users u ON u.id=f.artist_user_id
            WHERE cu.phone=?
            """,
            (client_phone,),
        ).fetchall()
        return {row["artist_phone"] for row in rows if row["artist_phone"]}


def add_favorite(client_phone: str, artist_phone: str):
    try:
        c.execute(
            "INSERT OR IGNORE INTO favorites(client_phone,artist_phone,created_at) VALUES(?,?,?)",
            (client_phone, artist_phone, now_iso()),
        )
    except sqlite3.OperationalError:
        # Legacy schema fallback
        client_row = c.execute("SELECT id FROM users WHERE phone=?", (client_phone,)).fetchone()
        artist_row = c.execute("SELECT id FROM users WHERE phone=?", (artist_phone,)).fetchone()
        if client_row and artist_row:
            c.execute(
                "INSERT OR IGNORE INTO favorites(user_id,artist_user_id,created_at) VALUES(?,?,?)",
                (client_row["id"], artist_row["id"], now_iso()),
            )


def remove_favorite(client_phone: str, artist_phone: str):
    try:
        c.execute(
            "DELETE FROM favorites WHERE client_phone=? AND artist_phone=?",
            (client_phone, artist_phone),
        )
    except sqlite3.OperationalError:
        client_row = c.execute("SELECT id FROM users WHERE phone=?", (client_phone,)).fetchone()
        artist_row = c.execute("SELECT id FROM users WHERE phone=?", (artist_phone,)).fetchone()
        if client_row and artist_row:
            c.execute(
                "DELETE FROM favorites WHERE user_id=? AND artist_user_id=?",
                (client_row["id"], artist_row["id"]),
            )


def get_favorites_display_rows(client_phone: str):
    try:
        return c.execute(
            """
            SELECT p.full_name, p.art, p.area, f.artist_phone
            FROM favorites f
            JOIN artist_profile p ON f.artist_phone=p.phone
            WHERE f.client_phone=? AND p.approval_status=1
            ORDER BY f.id DESC
            """,
            (client_phone,),
        ).fetchall()
    except sqlite3.OperationalError:
        return c.execute(
            """
            SELECT p.full_name, p.art, p.area, u.phone AS artist_phone
            FROM favorites f
            JOIN users cu ON cu.id=f.user_id
            JOIN users u ON u.id=f.artist_user_id
            JOIN artist_profile p ON p.phone=u.phone
            WHERE cu.phone=? AND p.approval_status=1
            ORDER BY f.id DESC
            """,
            (client_phone,),
        ).fetchall()


def add_portfolio_item_record(artist_phone: str, title: str, image_path: str):
    cols = _table_columns("portfolio_items")
    values = {"title": title.strip(), "image_path": image_path, "created_at": now_iso()}
    if "artist_phone" in cols:
        values["artist_phone"] = artist_phone
    if "user_id" in cols:
        row = c.execute("SELECT id FROM users WHERE phone=? LIMIT 1", (artist_phone,)).fetchone()
        if row and row["id"]:
            values["user_id"] = int(row["id"])
    if "description" in cols and "description" not in values:
        values["description"] = ""
    columns = ",".join(values.keys())
    placeholders = ",".join("?" for _ in values)
    c.execute(f"INSERT INTO portfolio_items({columns}) VALUES({placeholders})", tuple(values.values()))


def get_portfolio_items_by_artist(artist_phone: str, limit: int = None):
    cols = _table_columns("portfolio_items")
    if "artist_phone" in cols:
        sql = "SELECT * FROM portfolio_items WHERE artist_phone=? ORDER BY id DESC"
        params = [artist_phone]
    elif "user_id" in cols:
        row = c.execute("SELECT id FROM users WHERE phone=? LIMIT 1", (artist_phone,)).fetchone()
        user_id = int(row["id"]) if row and row["id"] else -1
        sql = "SELECT * FROM portfolio_items WHERE user_id=? ORDER BY id DESC"
        params = [user_id]
    else:
        return []
    if limit:
        sql += " LIMIT ?"
        params.append(limit)
    return c.execute(sql, tuple(params)).fetchall()


def create_booking_request(
    artist_phone: str,
    client_phone: str,
    client_name: str,
    client_email: str,
    message: str,
    event_date: str,
    budget: float,
):
    cols = _table_columns("bookings")
    values = {
        "event_date": event_date,
        "budget": float(budget),
        "message": message.strip(),
        "status": "pending",
        "created_at": now_iso(),
    }
    if "artist_phone" in cols:
        values["artist_phone"] = artist_phone
    if "artist_user_id" in cols:
        # Legacy compatibility: this ID may come from either `users` or `artist_users`.
        arow = c.execute("SELECT id FROM users WHERE phone=? LIMIT 1", (artist_phone,)).fetchone()
        if arow and arow["id"]:
            values["artist_user_id"] = int(arow["id"])
        else:
            legacy_artist = c.execute(
                "SELECT id FROM artist_users WHERE Phone_Number=? LIMIT 1",
                (artist_phone,),
            ).fetchone()
            if legacy_artist and legacy_artist["id"]:
                values["artist_user_id"] = int(legacy_artist["id"])
            else:
                values["artist_user_id"] = 0
    if "client_phone" in cols:
        values["client_phone"] = client_phone
    if "client_name" in cols:
        values["client_name"] = client_name.strip()
    if "client_email" in cols:
        values["client_email"] = client_email.strip()
    if "requester_name" in cols:
        values["requester_name"] = client_name.strip()
    if "requester_email" in cols:
        values["requester_email"] = client_email.strip() or "unknown@example.com"
    if "review_submitted" in cols:
        values["review_submitted"] = 0
    columns = ",".join(values.keys())
    placeholders = ",".join("?" for _ in values)
    c.execute(f"INSERT INTO bookings({columns}) VALUES({placeholders})", tuple(values.values()))


def get_bookings_for_artist(artist_phone: str):
    cols = _table_columns("bookings")
    conditions = []
    params = []
    if "artist_phone" in cols:
        conditions.append("artist_phone=?")
        params.append(artist_phone)
    if "artist_user_id" in cols:
        arow = c.execute("SELECT id FROM users WHERE phone=? LIMIT 1", (artist_phone,)).fetchone()
        if arow and arow["id"]:
            conditions.append("artist_user_id=?")
            params.append(int(arow["id"]))
        legacy_artist = c.execute(
            "SELECT id FROM artist_users WHERE Phone_Number=? LIMIT 1",
            (artist_phone,),
        ).fetchone()
        if legacy_artist and legacy_artist["id"]:
            conditions.append("artist_user_id=?")
            params.append(int(legacy_artist["id"]))
    if not conditions:
        return []
    sql = f"SELECT * FROM bookings WHERE ({' OR '.join(conditions)}) ORDER BY id DESC"
    return c.execute(sql, tuple(params)).fetchall()


def get_bookings_for_client(client_phone: str):
    cols = _table_columns("bookings")
    conditions = []
    params = []
    if "client_phone" in cols:
        conditions.append("client_phone=?")
        params.append(client_phone)
    if "requester_user_id" in cols:
        crow = c.execute("SELECT id FROM users WHERE phone=? LIMIT 1", (client_phone,)).fetchone()
        if crow and crow["id"]:
            conditions.append("requester_user_id=?")
            params.append(int(crow["id"]))
    if not conditions:
        return []
    sql = f"SELECT * FROM bookings WHERE ({' OR '.join(conditions)}) ORDER BY id DESC"
    return c.execute(sql, tuple(params)).fetchall()


def create_review(artist_phone: str, client_phone: str, rating: int, comment: str, booking_id: int = None):
    cols = _table_columns("reviews")
    values = {
        "rating": int(rating),
        "comment": comment.strip(),
        "created_at": now_iso(),
    }

    if "artist_phone" in cols:
        values["artist_phone"] = artist_phone
    if "client_phone" in cols:
        values["client_phone"] = client_phone
    if "booking_id" in cols:
        values["booking_id"] = booking_id
    if "reviewer_name" in cols:
        values["reviewer_name"] = client_phone or "guest_user"
    if "artist_user_id" in cols:
        row = c.execute("SELECT id FROM users WHERE phone=? LIMIT 1", (artist_phone,)).fetchone()
        values["artist_user_id"] = int(row["id"]) if row and row["id"] else 0

    columns = ",".join(values.keys())
    placeholders = ",".join("?" for _ in values)
    c.execute(f"INSERT INTO reviews({columns}) VALUES({placeholders})", tuple(values.values()))


def navigate_to(page: str):
    st.session_state.page = page
    st.rerun()


def render_global_nav(key_suffix: str, show_portal: bool = True, show_home: bool = True):
    st.markdown(
        "<div class='nav-blur'><div class='nav-title'>ArtLink</div>"
        "<div class='nav-crumb'>Where Creativity Meets Opportunity</div></div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div class='top-nav-wrap'>", unsafe_allow_html=True)
    cols = st.columns(6)
    labels_and_pages = [
        ("Home", "home"),
        ("Portals", "options"),
        ("Artist Portal", "artist"),
        ("User Portal", "user"),
        ("Admin Portal", "admin"),
        ("Top Artists", "top_artists"),
    ]
    for idx, (label, page) in enumerate(labels_and_pages):
        with cols[idx]:
            if st.button(label, key=f"top_nav_{key_suffix}_{page}", use_container_width=True):
                navigate_to(page)
    st.markdown("</div>", unsafe_allow_html=True)


def get_platform_snapshot():
    snapshot = {"artists": 0, "bookings": 0, "reviews": 0}
    try:
        artist_count = c.execute("SELECT COUNT(*) AS total FROM artist_profile").fetchone()
        booking_count = c.execute("SELECT COUNT(*) AS total FROM bookings").fetchone()
        review_count = c.execute("SELECT COUNT(*) AS total FROM reviews").fetchone()
        snapshot["artists"] = int(artist_count["total"] or 0) if artist_count else 0
        snapshot["bookings"] = int(booking_count["total"] or 0) if booking_count else 0
        snapshot["reviews"] = int(review_count["total"] or 0) if review_count else 0
    except Exception:
        pass
    return snapshot


def render_artist_spotlight_cards(limit: int = 6):
    artists = get_top_artists(limit=limit)
    if not artists:
        st.markdown(
            "<div class='empty-state'><h4>No featured artists yet</h4><p>Profiles will appear here as the marketplace grows.</p></div>",
            unsafe_allow_html=True,
        )
        return

    cards_html = ["<div class='artist-grid'>"]
    for art in artists:
        img_path = art.get("profile_image_path") if isinstance(art, dict) else art["profile_image_path"]
        if img_path and Path(img_path).exists():
            img_src = f"data:image/png;base64,{img_to_base64(img_path)}"
        else:
            img_src = f"data:image/png;base64,{img_to_base64('User.png')}"

        full_name = art.get("full_name") if isinstance(art, dict) else art["full_name"]
        artist_art = art.get("art") if isinstance(art, dict) else art["art"]
        avg_rating = art.get("avg_rating") if isinstance(art, dict) else art["avg_rating"]
        area = art.get("area") if isinstance(art, dict) else art["area"]
        description = art.get("description") if isinstance(art, dict) else art["description"]
        total_reviews = art.get("total_reviews", 0) if isinstance(art, dict) else art["total_reviews"]
        total_bookings = art.get("total_bookings", 0) if isinstance(art, dict) else art["total_bookings"]
        short_desc = (description or "Featured creator on ArtLink.")[:115]

        cards_html.append(
            f"<div class='artist-spotlight'>"
            f"<img src='{img_src}' alt='{full_name}'>"
            f"<div class='artist-topline'>"
            f"<div><div class='artist-name'>{full_name}</div><div class='artist-role'>{artist_art} | {area}</div></div>"
            f"<div class='artist-rating'>Top Rated {avg_rating}</div>"
            f"</div>"
            f"<div class='mini-note'>{short_desc}</div>"
            f"<div class='artist-stats'>"
            f"<span>{total_reviews} reviews</span>"
            f"<span>{total_bookings} bookings</span>"
            f"<span>Verified profile</span>"
            f"</div>"
            f"</div>"
        )
    cards_html.append("</div>")
    st.markdown("".join(cards_html), unsafe_allow_html=True)


def artist_register_ui():
    st.markdown("""
    <style>
        .stForm {
            background: linear-gradient(135deg, rgba(252,246,236,0.98) 0%, rgba(247,238,224,0.94) 100%) !important;
            border: 1px solid rgba(148,163,184,0.2) !important;
            border-radius: 20px !important;
            padding: 28px 32px !important;
            box-shadow: 0 16px 40px rgba(23,50,77,0.10) !important;
            max-width: 600px;
            margin: 0 auto;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.form("artist_registration"):
        st.markdown("<h3 style='text-align: center; margin-top: 0;'>Artist Registration</h3>", unsafe_allow_html=True)
        name = st.text_input("Name *", key="artist_reg_name")
        phone = st.text_input("Phone Number *", max_chars=10, key="artist_reg_phone")
        password = st.text_input("Create Password *", type="password", key="artist_reg_pass")
        confirm_password = st.text_input("Confirm Password *", type="password", key="artist_reg_confirm")
        
        submitted = st.form_submit_button("Register", use_container_width=True)
        
        if submitted:
            if not name.strip():
                st.error("Name is required")
            elif not validate_phone(phone):
                st.error("Enter valid 10 digit phone number")
            elif len(password) < 6:
                st.error("Password must be at least 6 characters")
            elif password != confirm_password:
                st.error("Passwords do not match")
            else:
                existing = c.execute("SELECT 1 FROM artist_users WHERE Phone_Number=?", (phone,)).fetchone()
                if existing:
                    st.warning("User already registered. Please login.")
                else:
                    c.execute(
                        "INSERT INTO artist_users(Name,Phone_Number,password_hash,created_at) VALUES(?,?,?,?)",
                        (name.strip(), phone, hash_password(password), now_iso()),
                    )
                    conn.commit()
                    st.toast("Registration complete", icon="✅")
                    st.success("Registration successful. Please login.")


def artist_login_ui():
    st.markdown("""
    <style>
        .stForm {
            background: linear-gradient(135deg, rgba(252,246,236,0.98) 0%, rgba(247,238,224,0.94) 100%) !important;
            border: 1px solid rgba(148,163,184,0.2) !important;
            border-radius: 20px !important;
            padding: 28px 32px !important;
            box-shadow: 0 16px 40px rgba(23,50,77,0.10) !important;
            max-width: 600px;
            margin: 0 auto;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.form("artist_login"):
        st.markdown("<h3 style='text-align: center; margin-top: 0;'>Artist Login</h3>", unsafe_allow_html=True)
        phone = st.text_input("Registered Phone Number", max_chars=10, key="artist_login_phone")
        password = st.text_input("Password", type="password", key="artist_login_password")
        
        submitted = st.form_submit_button("Login", use_container_width=True)
        
        if submitted:
            if not validate_phone(phone):
                st.error("Enter valid 10 digit phone number")
            elif not password:
                st.error("Password is required")
            else:
                row = c.execute(
                    "SELECT * FROM artist_users WHERE Phone_Number=? AND password_hash=?",
                    (phone, hash_password(password)),
                ).fetchone()
                if not row:
                    st.error("Invalid phone number or password")
                else:
                    st.session_state.artist_logged = True
                    st.session_state.artist_phone = phone
                    st.toast("Logged in", icon="✅")
                    st.rerun()


def artist_dashboard_ui():
    phone = st.session_state.artist_phone
    profile = get_profile(phone)

    status = profile["approval_status"] if profile else 0
    st.markdown(f"### Artist Dashboard {status_badge(status)}", unsafe_allow_html=True)
    avg_rating, total_reviews = rating_stats(phone)
    total_bookings = artist_booking_count(phone)
    s1, s2, s3 = st.columns(3)
    s1.markdown(
        f"<div class='stat-card'><div class='stat-value'>{total_bookings}</div><div class='stat-label'>Total Bookings</div></div>",
        unsafe_allow_html=True,
    )
    s2.markdown(
        f"<div class='stat-card'><div class='stat-value'>{avg_rating}</div><div class='stat-label'>Average Rating</div></div>",
        unsafe_allow_html=True,
    )
    s3.markdown(
        f"<div class='stat-card'><div class='stat-value'>{total_reviews}</div><div class='stat-label'>Reviews Received</div></div>",
        unsafe_allow_html=True,
    )

    tab1, tab2, tab3 = st.tabs(["Profile", "Portfolio", "Requests"])

    with tab1:
        if profile and not st.session_state.edit_mode:
            img_path = profile["profile_image_path"]
            if img_path and Path(img_path).exists():
                st.image(img_path, width=160)
            else:
                st.image("Artist.png", width=160)
            st.write("**Full Name:**", profile["full_name"])
            st.write("**Art Category:**", profile["art"])
            st.write("**Description:**", profile["description"])
            st.write("**Region:**", profile["area"])
            st.write("**Skills:**", profile["skills"] or "-")
            st.write("**Contact Email:**", profile["email"] or "-")
            st.write("**Portfolio Link:**", profile["drive"] or "-")
            st.caption("Updating profile sets status back to Pending for re-approval.")
            recent = artist_recent_reviews(phone, limit=4)
            if recent:
                st.markdown("#### Recent Reviews")
                for rv in recent:
                    st.write(f"⭐ {rv['rating']}/5 - {rv['comment'] or '-'}")

            c1, c2 = st.columns(2)
            with c1:
                if st.button("Edit Profile"):
                    st.session_state.edit_mode = True
                    st.rerun()
            with c2:
                if st.button("Logout"):
                    st.session_state.artist_logged = False
                    st.session_state.artist_phone = None
                    st.session_state.edit_mode = False
                    st.rerun()

        else:
            st.info("Create or update your profile")
            full_name_default = profile["full_name"] if profile else ""
            art_default = profile["art"] if profile else ""
            desc_default = profile["description"] if profile else ""
            area_default = profile["area"] if profile else ""
            drive_default = profile["drive"] if profile else ""
            skills_default = profile["skills"] if profile else ""
            email_default = profile["email"] if profile else ""
            image_default = profile["profile_image_path"] if profile else ""
            image_file = st.file_uploader("Profile Image", type=["jpg", "jpeg", "png"], key="profile_image_upload")
            if image_file is not None:
                st.image(image_file, width=160, caption="Preview")
            elif image_default and Path(image_default).exists():
                st.image(image_default, width=120, caption="Current Image")

            with st.form("artist_profile_form"):
                full_name = st.text_input("Full Name", value=full_name_default)
                art = st.selectbox(
                    "Art Category",
                    ["Music", "Dance", "Painting", "Theatre", "Photography", "Poetry", "Other"],
                    index=0,
                ) if not art_default else st.text_input("Art Category", value=art_default)
                desc = st.text_area("Art Description", value=desc_default)
                area = st.text_input("Region / Area", value=area_default)
                skills = st.text_input("Skills (comma separated)", value=skills_default)
                email = st.text_input("Contact Email", value=email_default)
                drive = st.text_input("Google Drive / Portfolio Link", value=drive_default)
                submit = st.form_submit_button("Save Profile")

            if submit:
                if not full_name.strip() or not art.strip() or not area.strip():
                    st.error("Full name, art category and region are required")
                else:
                    saved_image_path = image_default
                    if image_file is not None:
                        saved_image_path = save_uploaded_image(image_file, f"profile_{phone}")
                        if not saved_image_path:
                            st.error("Could not save profile image. Try another file.")
                            return
                    if profile:
                        c.execute(
                            """
                            UPDATE artist_profile
                            SET full_name=?, art=?, description=?, area=?, drive=?, skills=?, email=?, profile_image_path=?, approval_status=0, updated_at=?
                            WHERE phone=?
                            """,
                            (full_name, art, desc, area, drive, skills, email, saved_image_path, now_iso(), phone),
                        )
                    else:
                        c.execute(
                            """
                            INSERT INTO artist_profile(phone,full_name,art,description,area,drive,skills,email,profile_image_path,approval_status,updated_at)
                            VALUES(?,?,?,?,?,?,?,?,?,0,?)
                            """,
                            (phone, full_name, art, desc, area, drive, skills, email, saved_image_path, now_iso()),
                        )
                    conn.commit()
                    st.session_state.edit_mode = False
                    st.success("Profile saved and sent for admin approval")
                    st.rerun()

    with tab2:
        st.markdown("#### Upload Portfolio")
        with st.form("portfolio_upload_form"):
            title = st.text_input("Work Title")
            image_file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])
            upload = st.form_submit_button("Upload")

        if upload:
            if not title.strip() or image_file is None:
                st.error("Title and image are required")
            else:
                saved_path = save_uploaded_image(image_file, phone)
                if not saved_path:
                    st.error("Could not save image. Please try another file.")
                    return
                add_portfolio_item_record(phone, title.strip(), saved_path)
                conn.commit()
                st.success("Portfolio uploaded")
                st.rerun()

        st.markdown("#### Add Portfolio / Social Link")
        with st.form("portfolio_link_form"):
            platform = st.selectbox("Platform", ["Instagram", "YouTube", "Website", "Behance", "Other"])
            url = st.text_input("URL")
            add_link = st.form_submit_button("Add Link")
        if add_link:
            if not url.strip() or not (url.startswith("http://") or url.startswith("https://")):
                st.error("Enter a valid URL starting with http:// or https://")
            else:
                c.execute(
                    "INSERT INTO portfolio_links(artist_phone,platform,url,created_at) VALUES(?,?,?,?)",
                    (phone, platform, url.strip(), now_iso()),
                )
                conn.commit()
                st.success("Portfolio link added")
                st.rerun()

        items = get_portfolio_items_by_artist(phone)
        if items:
            cols = st.columns(3)
            for i, item in enumerate(items):
                with cols[i % 3]:
                    st.image(item["image_path"], use_container_width=True)
                    st.caption(item["title"])
        else:
            st.info("No portfolio items yet")

        links = c.execute(
            "SELECT * FROM portfolio_links WHERE artist_phone=? ORDER BY id DESC",
            (phone,),
        ).fetchall()
        if links:
            st.markdown("#### Portfolio Links")
            for link in links:
                st.markdown(f"- **{link['platform']}**: {link['url']}")

    with tab3:
        st.markdown("#### Incoming Requests")
        rows = get_bookings_for_artist(phone)
        if not rows:
            st.info("No booking requests yet")
        for row in rows:

            client_name = row["client_name"] if "client_name" in row.keys() and row["client_name"] else (
                row["requester_name"] if "requester_name" in row.keys() else "Guest"
            )
            client_email = row["client_email"] if "client_email" in row.keys() and row["client_email"] else (
                row["requester_email"] if "requester_email" in row.keys() else "-"
            )
            client_phone = row["client_phone"] if "client_phone" in row.keys() else None
            st.write(f"**Client:** {client_name} ({client_phone or 'Guest'})")
            st.write(f"**Email:** {client_email or '-'}")
            st.write(f"**Event Date:** {row['event_date'] or '-'}")
            st.write(f"**Budget:** ₹{int(row['budget'] or 0)}")
            st.write(f"**Message:** {row['message'] or '-'}")
            st.write(f"**Status:** {(row['status'] or '').title()}")

            a, b, d = st.columns(3)
            if a.button("Accept", key=f"acc_{row['id']}"):
                c.execute("UPDATE bookings SET status='accepted' WHERE id=?", (row["id"],))
                conn.commit()
                st.rerun()
            if b.button("Reject", key=f"rej_{row['id']}"):
                c.execute("UPDATE bookings SET status='rejected' WHERE id=?", (row["id"],))
                conn.commit()
                st.rerun()
            if d.button("Close", key=f"cls_{row['id']}"):
                c.execute("UPDATE bookings SET status='closed' WHERE id=?", (row["id"],))
                conn.commit()
                st.rerun()



def artist_page():
    render_global_nav("artist", show_portal=True, show_home=True)
    st.markdown("<h1 style='text-align:center;'>Artist Portal</h1>", unsafe_allow_html=True)
    _l, center, _r = st.columns([1, 2, 1])

    with center:
        if not st.session_state.artist_logged:
            mode = st.radio("Choose Option", ["Register", "Login"], horizontal=True)
            if mode == "Register":
                artist_register_ui()
            else:
                artist_login_ui()
        else:
            artist_dashboard_ui()


def client_register_ui():
    st.markdown("""
    <style>
        .stForm {
            background: linear-gradient(135deg, rgba(252,246,236,0.98) 0%, rgba(247,238,224,0.94) 100%) !important;
            border: 1px solid rgba(148,163,184,0.2) !important;
            border-radius: 20px !important;
            padding: 28px 32px !important;
            box-shadow: 0 16px 40px rgba(23,50,77,0.10) !important;
            max-width: 600px;
            margin: 0 auto;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.form("client_register_form"):
        st.markdown("<h3 style='text-align: center; margin-top: 0;'>User Sign Up</h3>", unsafe_allow_html=True)
        name = st.text_input("Name")
        phone = st.text_input("Phone", max_chars=10)
        password = st.text_input("Password", type="password")
        confirm = st.text_input("Confirm Password", type="password")
        submit = st.form_submit_button("Create Account", use_container_width=True)

    if submit:
        if not name.strip() or not validate_phone(phone):
            st.error("Enter valid name and phone")
            return
        if len(password) < 6:
            st.error("Password must be at least 6 characters")
            return
        if password != confirm:
            st.error("Passwords do not match")
            return

        exists = c.execute("SELECT 1 FROM client_users WHERE phone=?", (phone,)).fetchone()
        if exists:
            st.warning("Phone already registered. Please login")
            return

        c.execute(
            "INSERT INTO client_users(name,phone,password_hash,created_at) VALUES(?,?,?,?)",
            (name.strip(), phone, hash_password(password), now_iso()),
        )
        conn.commit()
        st.success("Account created. Please login.")


def client_login_ui():
    st.markdown("""
    <style>
        .stForm {
            background: linear-gradient(135deg, rgba(252,246,236,0.98) 0%, rgba(247,238,224,0.94) 100%) !important;
            border: 1px solid rgba(148,163,184,0.2) !important;
            border-radius: 20px !important;
            padding: 28px 32px !important;
            box-shadow: 0 16px 40px rgba(23,50,77,0.10) !important;
            max-width: 600px;
            margin: 0 auto;
        }
    </style>
    """, unsafe_allow_html=True)
    
    with st.form("client_login_form"):
        st.markdown("<h3 style='text-align: center; margin-top: 0;'>User Login</h3>", unsafe_allow_html=True)
        phone = st.text_input("Phone", max_chars=10)
        password = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login", use_container_width=True)

    if submit:
        if not validate_phone(phone):
            st.error("Enter valid 10 digit phone number")
            return
        row = c.execute("SELECT * FROM client_users WHERE phone=?", (phone,)).fetchone()
        if not row or row["password_hash"] != hash_password(password):
            st.error("Invalid credentials")
            return

        st.session_state.client_logged = True
        st.session_state.client_phone = phone
        st.toast("Login successful", icon="✅")
        st.rerun()


def admin_page():
    render_global_nav("admin", show_portal=True, show_home=True)
    st.title("Admin Panel")

    admin_user = st.secrets.get("ADMIN_USERNAME", "admin") if hasattr(st, "secrets") else "admin"
    admin_pass = st.secrets.get("ADMIN_PASSWORD", "admin@123") if hasattr(st, "secrets") else "admin@123"

    if not st.session_state.admin_logged:
        st.markdown("""
        <style>
            .stForm {
                background: linear-gradient(135deg, rgba(252,246,236,0.98) 0%, rgba(247,238,224,0.94) 100%) !important;
                border: 1px solid rgba(148,163,184,0.2) !important;
                border-radius: 20px !important;
                padding: 28px 32px !important;
                box-shadow: 0 16px 40px rgba(23,50,77,0.10) !important;
                max-width: 600px;
                margin: 0 auto;
            }
        </style>
        """, unsafe_allow_html=True)
        
        with st.form("admin_login_form"):
            st.markdown("<h3 style='text-align: center; margin-top: 0;'>Admin Login</h3>", unsafe_allow_html=True)
            u = st.text_input("Admin Username")
            p = st.text_input("Admin Password", type="password")
            submit = st.form_submit_button("Login", use_container_width=True)
        if submit:
            if u == admin_user and p == admin_pass:
                st.session_state.admin_logged = True
                st.success("Admin login successful")
                st.rerun()
            else:
                st.error("Invalid admin credentials")
        return

    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Approvals", "Users", "Bookings", "Reviews", "Top Artists"])

    with tab1:
        f1, f2 = st.columns([2, 3])
        status_filter = f1.selectbox("Filter by Status", ["All", "Pending", "Approved", "Rejected"])
        query_map = {
            "All": "SELECT * FROM artist_profile ORDER BY id DESC",
            "Pending": "SELECT * FROM artist_profile WHERE approval_status=0 ORDER BY id DESC",
            "Approved": "SELECT * FROM artist_profile WHERE approval_status=1 ORDER BY id DESC",
            "Rejected": "SELECT * FROM artist_profile WHERE approval_status=-1 ORDER BY id DESC",
        }
        rows = c.execute(query_map[status_filter]).fetchall()
        if not rows:
            st.info("No pending artists")
        for row in rows:

            st.markdown(
                f"<div class='artist-name'>{row['full_name'] or '-'} {status_badge(row['approval_status'] or 0)}</div>",
                unsafe_allow_html=True,
            )
            st.write(f"Phone: {row['phone']}")
            st.write(f"Art: {row['art']} | Region: {row['area']}")
            status = int(row["approval_status"] or 0)
            if status == 0:
                x, y = st.columns(2)
                if x.button("Approve", key=f"approve_{row['phone']}"):
                    c.execute("UPDATE artist_profile SET approval_status=1 WHERE phone=?", (row["phone"],))
                    conn.commit()
                    st.toast("Artist approved", icon="✅")
                    st.rerun()
                if y.button("Reject", key=f"reject_{row['phone']}"):
                    c.execute("UPDATE artist_profile SET approval_status=-1 WHERE phone=?", (row["phone"],))
                    conn.commit()
                    st.toast("Artist rejected", icon="⛔")
                    st.rerun()
            elif status == 1:
                st.success("Already approved")
            else:
                st.warning("Already rejected")


    with tab2:
        st.markdown("#### Registered Artists")
        artists = c.execute("SELECT Name, Phone_Number FROM artist_users ORDER BY id DESC").fetchall()
        st.dataframe([dict(r) for r in artists], use_container_width=True)

        st.markdown("#### Registered Users")
        users = c.execute("SELECT name, phone, created_at FROM client_users ORDER BY id DESC").fetchall()
        st.dataframe([dict(r) for r in users], use_container_width=True)

    with tab3:
        rows = c.execute("SELECT * FROM bookings ORDER BY id DESC").fetchall()
        st.dataframe([dict(r) for r in rows], use_container_width=True)

    with tab4:
        try:
            rows = c.execute(
                """
                SELECT r.rating, r.comment, r.created_at, r.client_phone, p.full_name AS artist_name
                FROM reviews r
                LEFT JOIN artist_profile p ON p.phone=r.artist_phone
                ORDER BY r.id DESC
                """
            ).fetchall()
        except sqlite3.OperationalError:
            # Backward compatibility for older DB schemas.
            rows = c.execute(
                """
                SELECT r.rating, r.comment, r.created_at, '' AS client_phone, p.full_name AS artist_name
                FROM reviews r
                LEFT JOIN artist_profile p ON p.phone=r.artist_phone
                ORDER BY r.id DESC
                """
            ).fetchall()
        if not rows:
            st.info("No reviews yet")
        for rv in rows:

            st.write(f"**Artist:** {rv['artist_name'] or '-'}")
            st.write(f"**Rating:** {'⭐' * int(rv['rating'])} ({rv['rating']}/5)")
            st.write(f"**Comment:** {rv['comment'] or '-'}")
            st.caption(f"By {rv['client_phone'] or 'guest'} on {rv['created_at']}")


    with tab5:
        featured = get_top_artists(limit=10)
        if not featured:
            st.info("No top artists data yet")
        for art in featured:

            st.markdown(f"**{art['full_name']}** {status_badge(1)}", unsafe_allow_html=True)
            st.write(f"Art: {art['art']} | Region: {art['area']}")
            st.write(f"Rating: ⭐ {art['avg_rating']} ({art['total_reviews']} reviews)")
            st.write(f"Bookings: {art['total_bookings']}")


    if st.button("Admin Logout"):
        st.session_state.admin_logged = False
        st.rerun()


def user_page():
    render_global_nav("user", show_portal=True, show_home=True)
    st.title("Available Artists")

    left_space, auth_col, right_space = st.columns([1, 2.2, 1])
    with auth_col:
        if not st.session_state.client_logged:
            auth_mode = st.radio("Choose Option", ["Login", "Sign Up"], horizontal=True, key="user_auth_mode")
            if auth_mode == "Login":
                client_login_ui()
            else:
                client_register_ui()
        else:
            st.success(f"Logged in as {st.session_state.client_phone}")
            if st.button("Logout User"):
                st.session_state.client_logged = False
                st.session_state.client_phone = None
                st.rerun()

    if st.session_state.client_logged:
        st.info("User Portal: Use **Booking Portal** to send requests and **Review Portal** to rate booked artists.")
    else:
        st.warning("Login as user to access Booking Portal and Review Portal.")

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    if st.session_state.client_logged:
        st.markdown("### Booking Portal")
    else:
        st.markdown("### Discover Artists")
    st.markdown("#### Search & Filters")
    f1, f2, f3 = st.columns(3)
    q_name = f1.text_input("Search by Name")
    q_art = f2.text_input("Filter by Category")
    q_area = f3.text_input("Filter by Location")

    query = """
        SELECT p.*
        FROM artist_profile p
        WHERE p.approval_status=1
          AND LOWER(p.full_name) LIKE ?
          AND LOWER(p.art) LIKE ?
          AND LOWER(p.area) LIKE ?
        ORDER BY p.id DESC
    """
    artists = c.execute(
        query,
        (
            f"%{q_name.lower().strip()}%",
            f"%{q_art.lower().strip()}%",
            f"%{q_area.lower().strip()}%",
        ),
    ).fetchall()

    if not artists:
        st.markdown(
            "<div class='empty-state'><h4>No artists found</h4><p>Try adjusting name, category, or region filters.</p></div>",
            unsafe_allow_html=True,
        )
        return

    fav_set = set()
    if st.session_state.client_logged:
        fav_set = get_favorite_artist_phones(st.session_state.client_phone)

    cols = st.columns(2)
    for i, artist in enumerate(artists):
        avg_rating, count_rating = rating_stats(artist["phone"])
        with cols[i % 2]:

            profile_img = artist["profile_image_path"] if "profile_image_path" in artist.keys() else None
            if profile_img and Path(profile_img).exists():
                st.image(profile_img, width=95)
            else:
                st.image("User.png", width=95)
            st.markdown(
                f"<div class='artist-name'>{artist['full_name']} {status_badge(1)}</div>",
                unsafe_allow_html=True,
            )
            st.markdown(f"<b>Art:</b> {artist['art']}<br>", unsafe_allow_html=True)
            st.markdown(f"<b>Description:</b> {artist['description']}<br>", unsafe_allow_html=True)
            st.markdown(f"<b>Region:</b> {artist['area']}<br>", unsafe_allow_html=True)
            st.markdown(f"<b>Contact Phone:</b> {artist['phone']}<br>", unsafe_allow_html=True)
            st.markdown(f"<b>Contact Email:</b> {artist['email'] or '-'}<br>", unsafe_allow_html=True)
            st.markdown(f"<b>Skills:</b> {artist['skills'] or '-'}<br>", unsafe_allow_html=True)
            st.markdown(f"<b>Portfolio Link:</b> {artist['drive'] or '-'}<br>", unsafe_allow_html=True)
            st.markdown(
                f"<b>Rating:</b> {avg_rating}/5 ({count_rating} reviews)<br>",
                unsafe_allow_html=True,
            )

            p_items = get_portfolio_items_by_artist(artist["phone"], limit=3)
            if p_items:
                st.caption("Portfolio Preview")
                pcols = st.columns(3)
                for j, item in enumerate(p_items):
                    with pcols[j % 3]:
                        st.image(item["image_path"], use_container_width=True)

            link_rows = c.execute(
                "SELECT platform, url FROM portfolio_links WHERE artist_phone=? ORDER BY id DESC LIMIT 4",
                (artist["phone"],),
            ).fetchall()
            if link_rows:
                st.caption("Portfolio / Social Links")
                for link in link_rows:
                    st.markdown(f"- **{link['platform']}**: {link['url']}")

            if st.session_state.client_logged:
                fav_label = "Remove Favorite" if artist["phone"] in fav_set else "Add Favorite"
                if st.button(fav_label, key=f"fav_btn_{artist['phone']}"):
                    if artist["phone"] in fav_set:
                        remove_favorite(st.session_state.client_phone, artist["phone"])
                        st.toast("Removed from favorites", icon="💔")
                    else:
                        add_favorite(st.session_state.client_phone, artist["phone"])
                        st.toast("Added to favorites", icon="❤️")
                    conn.commit()
                    st.rerun()

                st.markdown(f"""
                <style>
                    [data-testid="stForm"] {{
                        background: linear-gradient(135deg, rgba(252,246,236,0.98) 0%, rgba(247,238,224,0.94) 100%) !important;
                        border: 1px solid rgba(148,163,184,0.2) !important;
                        border-radius: 20px !important;
                        padding: 28px 32px !important;
                        box-shadow: 0 16px 40px rgba(23,50,77,0.10) !important;
                    }}
                </style>
                """, unsafe_allow_html=True)
                
                with st.form(f"book_form_{artist['phone']}"):
                    st.markdown("<h4 style='margin-top: 0; text-align: center;'>Book this Artist</h4>", unsafe_allow_html=True)
                    client_name = st.text_input("Your Name", key=f"book_name_{artist['phone']}")
                    client_email = st.text_input("Your Email", key=f"book_email_{artist['phone']}")
                    event_date = st.date_input("Event Date", key=f"book_date_{artist['phone']}")
                    budget = st.number_input("Budget", min_value=0.0, step=500.0, key=f"book_budget_{artist['phone']}")
                    message = st.text_area("Message", key=f"book_msg_{artist['phone']}")
                    submit = st.form_submit_button("Send Request", use_container_width=True)
                
                if submit:
                    if not client_name.strip():
                        st.error("Client name is required")
                    elif client_email and ("@" not in client_email or "." not in client_email):
                        st.error("Enter a valid email")
                    else:
                        create_booking_request(
                            artist_phone=artist["phone"],
                            client_phone=st.session_state.client_phone,
                            client_name=client_name.strip(),
                            client_email=client_email.strip(),
                            message=message.strip(),
                            event_date=str(event_date),
                            budget=float(budget),
                        )
                        conn.commit()
                        st.toast("Request sent", icon="✅")
                        st.success("Booking request sent")

                st.caption("Reviews can be submitted from your booking history after placing a request.")

            revs = c.execute(
                "SELECT rating, comment, created_at FROM reviews WHERE artist_phone=? ORDER BY id DESC LIMIT 2",
                (artist["phone"],),
            ).fetchall()
            if revs:
                st.caption("Latest Reviews")
                for rv in revs:
                    st.write(f"⭐ {rv['rating']}/5 - {rv['comment'] or '-'}")



    if st.session_state.client_logged:
        st.markdown("### Your Favorites")
        favs = get_favorites_display_rows(st.session_state.client_phone)
        if not favs:
            st.info("No favorites yet")
        else:
            for f in favs:
                st.write(f"• {f['full_name']} ({f['art']}, {f['area']})")

        st.markdown("### Review Portal")
        st.markdown("#### Your Bookings & Reviews")
        my_bookings = get_bookings_for_client(st.session_state.client_phone)
        if not my_bookings:
            st.info("No bookings yet")
        for bk in my_bookings:

            artist_phone = bk["artist_phone"] if "artist_phone" in bk.keys() else None
            if not artist_phone and "artist_user_id" in bk.keys() and bk["artist_user_id"]:
                arow = c.execute("SELECT phone FROM users WHERE id=?", (bk["artist_user_id"],)).fetchone()
                artist_phone = arow["phone"] if arow else ""
            artist_profile = c.execute(
                "SELECT full_name, art FROM artist_profile WHERE phone=?",
                (artist_phone,),
            ).fetchone() if artist_phone else None
            artist_name = artist_profile["full_name"] if artist_profile else (artist_phone or "Unknown Artist")
            artist_art = artist_profile["art"] if artist_profile else "-"
            st.write(f"**Artist:** {artist_name} ({artist_art})")
            st.write(f"**Artist Contact:** {artist_phone or '-'}")
            st.write(f"**Event:** {bk['event_date'] or '-'} | **Budget:** ₹{int(bk['budget'] or 0)}")
            st.write(f"**Status:** {(bk['status'] or '').title()}")
            st.write(f"**Message:** {bk['message'] or '-'}")
            if int(bk["review_submitted"] or 0) == 0:
                with st.form(f"book_review_form_{bk['id']}"):
                    st.markdown("#### Submit Review")
                    rating = st.slider("Rating", 1, 5, 5, key=f"bk_rate_{bk['id']}")
                    comment = st.text_area("Comment", key=f"bk_comment_{bk['id']}")
                    submit_review = st.form_submit_button("Submit Review")
                    if submit_review:
                        if not comment.strip():
                            st.error("Please add a review comment")
                        else:
                            create_review(
                                artist_phone=artist_phone or "",
                                client_phone=st.session_state.client_phone,
                                rating=int(rating),
                                comment=comment.strip(),
                                booking_id=bk["id"],
                            )
                            c.execute("UPDATE bookings SET review_submitted=1 WHERE id=?", (bk["id"],))
                            conn.commit()
                        st.toast("Review submitted", icon="⭐")
                        st.rerun()
            else:
                st.success("Review submitted for this booking")



def home_page():
    render_global_nav("home", show_portal=True, show_home=False)
    snapshot = get_platform_snapshot()

    left, right = st.columns([1.2, 0.8], gap="large")
    with left:
        st.markdown(
            f"""
            <div class="hero">
                <div class="brand-chip">Creative Talent Network</div>
                <h1>Beautiful artist portfolios. Effortless event bookings. One polished destination.</h1>
                <p>ArtLink helps performers and clients meet in a space that feels curated, trusted, and ready for real opportunities. Artists build presence, clients book with confidence, and admins keep quality high.</p>
                <div class="hero-kpis">
                    <span class="kpi-chip"><strong>{snapshot['artists'] or '100+'}</strong> artist profiles live</span>
                    <span class="kpi-chip"><strong>{snapshot['bookings'] or '50+'}</strong> booking moments created</span>
                    <span class="kpi-chip"><strong>{snapshot['reviews'] or '4.8/5'}</strong> signals of trust</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1.1, 1.1, 1.2])
        with c1:
            if st.button("Enter Portals", key="home_enter_portals", use_container_width=True):
                st.session_state.page = "options"
                st.rerun()
        with c2:
            if st.button("Browse Artists", key="home_browse_artists", use_container_width=True):
                st.session_state.page = "top_artists"
                st.rerun()

    with right:
        logo64 = img_to_base64("Logo.png")
        st.markdown(
            f"""
            <div class='home-visual-card'>
                <div class='home-logo-stage'>
                    <img src='data:image/png;base64,{logo64}' alt='ArtLink logo'>
                </div>
                <div class='home-metrics-grid'>
                    <div class='hero-metric'><strong>{max(snapshot['artists'], 12)}</strong><span>Creative profiles ready to explore</span></div>
                    <div class='hero-metric'><strong>{max(snapshot['bookings'], 8)}</strong><span>Booking conversations captured</span></div>
                    <div class='hero-metric'><strong>{max(snapshot['reviews'], 6)}</strong><span>Community reviews shared</span></div>
                    <div class='hero-metric'><strong>24/7</strong><span>Digital presence for every artist</span></div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='feature-band'>
            <div class='feature-tile'>
                <strong>For Artists</strong>
                <p>Present your work with a stronger first impression, collect reviews, and manage incoming requests from one place.</p>
            </div>
            <div class='feature-tile'>
                <strong>For Clients</strong>
                <p>Discover verified talent by category and city, compare profiles quickly, and reach out with confidence.</p>
            </div>
            <div class='feature-tile'>
                <strong>For Teams</strong>
                <p>Keep quality high through approvals, featured placements, and a marketplace flow that feels more trustworthy.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div class='section-title'>Featured Talent</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>A quick look at some of the strongest profiles on the platform.</div>", unsafe_allow_html=True)
    render_artist_spotlight_cards(limit=3)


def options_page():
    render_global_nav("options", show_portal=False, show_home=True)
    st.markdown(
        """
        <div class="hero">
            <div class="brand-chip">Trusted by performers and event teams</div>
            <h1>Build, Book, and Grow with Verified Creative Talent</h1>
            <p>From standout artist pages to smoother client discovery, this experience now feels more like a creative brand than a plain dashboard.</p>
            <div class="hero-kpis">
                <span class="kpi-chip"><strong>Artist-first</strong> portfolio experience</span>
                <span class="kpi-chip"><strong>Fast</strong> booking workflows</span>
                <span class="kpi-chip"><strong>Quality</strong> moderation and reviews</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)
    cta1, cta2 = st.columns(2)
    with cta1:
        if st.button("Get Started", key="hero_get_started", use_container_width=True):
            st.session_state.page = "artist"
            st.rerun()
    with cta2:
        if st.button("Explore Artists", key="hero_explore_artists", use_container_width=True):
            st.session_state.page = "user"
            st.rerun()

    st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='feature-band'>
            <div class='feature-tile'>
                <strong>Launch a polished profile</strong>
                <p>Artists can tell a stronger story with images, descriptions, and social proof that feels client-ready.</p>
            </div>
            <div class='feature-tile'>
                <strong>Book with less friction</strong>
                <p>Users move from browsing to inquiry quickly, with trust signals placed where they matter most.</p>
            </div>
            <div class='feature-tile'>
                <strong>Keep quality visible</strong>
                <p>Admin review, featured sections, and ratings combine to create a more premium marketplace atmosphere.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class='portal-section-head'>
            <h2>Choose Your Portal</h2>
            <p>Each portal now feels more intentional, with a clearer path for artists, clients, and platform admins.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    artist64 = img_to_base64("Artist.png")
    user64 = img_to_base64("User.png")
    admin64 = img_to_base64("Logo.png")
    top64 = img_to_base64("Artist.png")

    row1 = st.columns(2)
    with row1[0]:
        st.markdown(
            f"""
            <div class='portal-card'>
                <div class='portal-meta'><h3>Artist Portal</h3><p>Showcase your talent, manage bookings, and build credibility.</p></div>
                <div class='portal-media'><img src='data:image/png;base64,{artist64}'></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open Artist", key="open_artist", use_container_width=True):
            st.session_state.page = "artist"
            st.rerun()

    with row1[1]:
        st.markdown(
            f"""
            <div class='portal-card'>
                <div class='portal-meta'><h3>User Portal</h3><p>Explore verified artists, send booking requests, and leave reviews.</p></div>
                <div class='portal-media'><img src='data:image/png;base64,{user64}'></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open User", key="open_user", use_container_width=True):
            st.session_state.page = "user"
            st.rerun()

    row2 = st.columns(2)
    with row2[0]:
        st.markdown(
            f"""
            <div class='portal-card'>
                <div class='portal-meta'><h3>Admin Portal</h3><p>Approve artists, review platform activity, and manage quality.</p></div>
                <div class='portal-media'><img src='data:image/png;base64,{admin64}'></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Open Admin", key="open_admin", use_container_width=True):
            st.session_state.page = "admin"
            st.rerun()

    with row2[1]:
        st.markdown(
            f"""
            <div class='portal-card'>
                <div class='portal-meta'><h3>Top Artists</h3><p>Meet the highest-rated artists and featured performers.</p></div>
                <div class='portal-media'><img src='data:image/png;base64,{top64}'></div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("View Top Artists", key="open_top_artists", use_container_width=True):
            st.session_state.page = "top_artists"
            st.rerun()

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Live Activity</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Real-time updates from across the platform.</div>", unsafe_allow_html=True)
    events = [
        "New artist registered: Sneha Dancer",
        "User booked Rahul Musician",
        "Top Artist badge awarded to Aditi Painter",
        "New 5-star review for Arjun Percussionist",
        "Booking accepted by Rushi Parhad",
        "Portfolio updated by Meera Vocalist",
    ]
    components.html(
        f"""
        <div class="live-feed">
            <div class="live-item show" id="live-item">
                <span class="live-dot"></span>
                <span id="live-text"></span>
            </div>
        </div>
        <script>
        const events = {json.dumps(events)};
        let idx = 0;
        const textEl = document.getElementById("live-text");
        const itemEl = document.getElementById("live-item");
        function rotateEvent() {{
            itemEl.classList.remove("show");
            setTimeout(() => {{
                textEl.textContent = events[idx % events.length];
                itemEl.classList.add("show");
                idx += 1;
            }}, 140);
        }}
        rotateEvent();
        setInterval(rotateEvent, 2500);
        </script>
        """,
        height=110,
    )

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("<div class='section-title'>Top Artists</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Featured performers with the highest ratings.</div>", unsafe_allow_html=True)
    render_artist_spotlight_cards(limit=4)


def top_artists_page():
    render_global_nav("top_artists", show_portal=True, show_home=True)
    st.markdown(
        """
        <div class="hero">
            <div class="brand-chip">Featured Lineup</div>
            <h1>Meet the artists creating the strongest first impression on ArtLink.</h1>
            <p>These profiles stand out for quality, consistency, reviews, and booking momentum across the platform.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    with st.spinner("Loading top artists..."):
        artists = get_top_artists(limit=8)

    if not artists:
        st.markdown(
            "<div class='empty-state'><h4>No top artists available</h4><p>Please check again later.</p></div>",
            unsafe_allow_html=True,
        )
        return

    st.markdown("<div class='section-title'>Top Artists</div>", unsafe_allow_html=True)
    st.markdown("<div class='section-sub'>Browse the standout creators people are most likely to trust and book.</div>", unsafe_allow_html=True)
    render_artist_spotlight_cards(limit=8)

    if st.button("Back to Options", use_container_width=True):
        st.session_state.page = "options"
        st.rerun()


def route():
    query = st.query_params
    if "nav" in query:
        if query["nav"] == "artist":
            st.session_state.page = "artist"
        elif query["nav"] == "user":
            st.session_state.page = "user"
        elif query["nav"] == "admin":
            st.session_state.page = "admin"
        elif query["nav"] == "top_artists":
            st.session_state.page = "top_artists"

    if st.session_state.page == "home":
        home_page()
    elif st.session_state.page == "options":
        options_page()
    elif st.session_state.page == "artist":
        artist_page()
    elif st.session_state.page == "admin":
        admin_page()
    elif st.session_state.page == "top_artists":
        top_artists_page()
    else:
        user_page()


db_init()
seed_existing_artists_passwords()
bootstrap_state()
route()



