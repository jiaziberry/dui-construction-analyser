#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Chinese 对-Construction Analyser
================================
A learner-focused web application for understanding Chinese 对-constructions.

Designed for non-native speakers to:
1. Look up how predicates are used in real Chinese (based on 394,355 corpus instances)
2. Understand WHY a sentence is classified a certain way
3. Learn the six construction types with clear explanations
"""

import streamlit as st
import pandas as pd
import json
import os

# Import utilities
from utils.corpus_lookup import (
    CorpusLookup, 
    TYPE_NAMES, 
    TYPE_EXPLANATIONS,
    get_type_name,
    get_type_explanation
)
from utils.construction_info import CONSTRUCTION_TYPES, COMPARISON_TABLE, KEY_DISTINCTIONS
from utils.predicate_extractor import extract_dui_parts, guess_y_animacy

# Page configuration
st.set_page_config(
    page_title="Chinese 对-Construction Analyser",
    page_icon="🇨🇳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .type-card {
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 5px solid;
    }
    .corpus-stat {
        background-color: #f0f2f6;
        padding: 10px;
        border-radius: 5px;
        margin: 5px 0;
    }
    .learning-tip {
        background-color: #e8f4ea;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #4CAF50;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_corpus_lookup():
    """Get cached corpus lookup instance."""
    return CorpusLookup()


def main():
    """Main application."""
    with st.sidebar:
        st.title("🇨🇳 Navigation")
        page = st.radio(
            "Choose a page:",
            [
                "🏠 Home",
                "🔍 Analyse Sentence",
                "📖 Look Up Predicate",
                "📚 Learn the Six Types",
                "📊 Corpus Statistics",
                "❓ Help"
            ]
        )
        
        st.divider()
        st.markdown("### About")
        st.markdown("""
        This tool helps you understand Chinese **对** (duì) constructions 
        using data from **394,355** real examples from the BCC corpus.
        """)
    
    if page == "🏠 Home":
        show_home()
    elif page == "🔍 Analyse Sentence":
        show_analysis()
    elif page == "📖 Look Up Predicate":
        show_predicate_lookup()
    elif page == "📚 Learn the Six Types":
        show_learning()
    elif page == "📊 Corpus Statistics":
        show_statistics()
    elif page == "❓ Help":
        show_help()


def show_home():
    """Home page."""
    st.title("🇨🇳 Chinese 对-Construction Analyser")
    
    st.markdown("""
    ## Welcome! 欢迎！
    
    This tool helps you understand how the Chinese preposition **对** (duì) works.
    
    In Chinese, 对 can be used in **six different ways**, and understanding which 
    one is being used helps you understand the meaning correctly.
    """)
    
    # Quick overview of types
    st.markdown("### The Six Types at a Glance")
    
    cols = st.columns(3)
    type_order = ['DA', 'SI', 'MS', 'ABT', 'EVAL', 'DISP']
    
    for i, code in enumerate(type_order):
        info = CONSTRUCTION_TYPES.get(code, {})
        with cols[i % 3]:
            colour = info.get('colour', '#808080')
            st.markdown(f"""
            <div style="background: {colour}20; padding: 12px; border-radius: 8px; 
                        border-left: 4px solid {colour}; margin: 5px 0;">
                <strong>{info.get('emoji', '')} {info.get('full_name', code)}</strong><br>
                <span style="color: #666; font-size: 0.9em;">{info.get('chinese_name', '')}</span><br>
                <span style="font-size: 0.85em;">{info.get('short_description', '')}</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Quick start
    st.markdown("### 🚀 Quick Start")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Analyse a sentence:**
        
        Enter any Chinese sentence with 对 and see:
        - Which construction type it is
        - How this predicate is used in real Chinese
        - Why it's classified this way
        """)
    
    with col2:
        st.markdown("""
        **Look up a predicate:**
        
        Search for any verb/adjective to see:
        - How often it appears with 对
        - Which types it's used with
        - Similar predicates
        """)


def show_analysis():
    """Sentence analysis page."""
    st.title("🔍 Analyse Your Sentence")
    
    st.markdown("""
    Enter a Chinese sentence containing **对** and I'll help you understand 
    what construction type it is and why.
    """)
    
    # Input
    sentence = st.text_input(
        "Enter a Chinese sentence with 对:",
        placeholder="例如：专家对此发表意见",
    )
    
    # Example buttons
    st.markdown("**Or try an example:**")
    examples = [
        ("专家对此发表意见", "ABT"),
        ("他对我说了几句话", "DA"),
        ("政府对企业进行检查", "SI"),
        ("我对这件事很担心", "MS"),
        ("她对客人很热情", "DISP"),
        ("运动对健康有益", "EVAL"),
    ]
    
    cols = st.columns(3)
    for i, (ex, _) in enumerate(examples):
        with cols[i % 3]:
            if st.button(ex, key=f"ex_{i}"):
                sentence = ex
    
    if sentence and '对' in sentence:
        analyse_sentence(sentence)
    elif sentence:
        st.warning("⚠️ Please enter a sentence containing 对")


def analyse_sentence(sentence: str):
    """Analyse a sentence and display results."""
    st.markdown("---")
    
    # Extract parts
    parts = extract_dui_parts(sentence)
    predicate = parts.get('predicate', '')
    complement = parts.get('after_predicate', '')
    y_phrase = parts.get('y_phrase', '')
    
    # Get corpus lookup
    lookup = get_corpus_lookup()
    
    # Contextual analysis
    analysis = lookup.analyse_in_context(
        predicate, 
        complement=complement,
        y_phrase=y_phrase,
        full_sentence=sentence
    )
    
    result_type = analysis.get('contextual_type', 'DA')
    info = CONSTRUCTION_TYPES.get(result_type, {})
    colour = info.get('colour', '#808080')
    
    # Main result
    st.markdown(f"""
    <div style="background: {colour}20; padding: 25px; border-radius: 15px; 
                border-left: 6px solid {colour};">
        <h2 style="margin: 0;">{info.get('emoji', '')} {info.get('full_name', result_type)}</h2>
        <p style="font-size: 1.2em; color: #666; margin: 5px 0;">{info.get('chinese_name', '')}</p>
        <p style="margin-top: 15px;"><strong>Your sentence:</strong> {sentence}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Why this classification?
    st.markdown("### 💡 Why this classification?")
    
    if analysis.get('contextual_reason'):
        st.info(analysis['contextual_reason'])
    
    # Type explanation
    type_exp = TYPE_EXPLANATIONS.get(result_type, {})
    if type_exp:
        st.markdown(f"""
        <div class="learning-tip">
            <strong>Understanding {info.get('full_name', '')}:</strong><br>
            {type_exp.get('description', '')}<br><br>
            <strong>Y's role:</strong> {type_exp.get('y_role', '')}<br><br>
            <strong>Test:</strong> {type_exp.get('test', '')}
        </div>
        """, unsafe_allow_html=True)
    
    # Corpus data for predicate
    if predicate:
        st.markdown(f"### 📊 How is '{predicate}' used in real Chinese?")
        
        corpus_data = analysis.get('corpus_data', {})
        if corpus_data:
            total = corpus_data.get('total', 0)
            st.markdown(f"Found **{total:,}** instances of '**{predicate}**' with 对 in the BCC corpus:")
            
            # Distribution chart
            dist = corpus_data.get('distribution', {})
            if dist:
                chart_data = []
                for type_code, pct in sorted(dist.items(), key=lambda x: x[1], reverse=True):
                    if pct > 0:
                        full_name, _ = TYPE_NAMES.get(type_code, (type_code, ''))
                        chart_data.append({'Type': full_name, 'Percentage': pct})
                
                if chart_data:
                    df = pd.DataFrame(chart_data)
                    st.bar_chart(df.set_index('Type'))
                    
                    # Text explanation
                    dominant = corpus_data.get('dominant_type', '')
                    conf = corpus_data.get('confidence', 0)
                    dominant_name, _ = TYPE_NAMES.get(dominant, (dominant, ''))
                    
                    if conf >= 0.9:
                        st.success(f"'{predicate}' is almost always **{dominant_name}** ({conf*100:.0f}% of cases)")
                    elif conf >= 0.6:
                        st.info(f"'{predicate}' is usually **{dominant_name}** ({conf*100:.0f}% of cases), but can be other types depending on context")
                    else:
                        st.warning(f"'{predicate}' varies a lot by context! Most common is {dominant_name} ({conf*100:.0f}%), but other types are also frequent")
        else:
            st.info(f"'{predicate}' was not found in the corpus. Classification based on rules.")
    
    # Learning notes
    if analysis.get('learning_notes'):
        st.markdown("### 📝 Learning Notes")
        for note in analysis['learning_notes']:
            if note:
                st.markdown(f"- {note}")


def show_predicate_lookup():
    """Predicate lookup page."""
    st.title("📖 Look Up a Predicate")
    
    st.markdown("""
    Search for any Chinese verb or adjective to see how it's typically used 
    with 对 in real Chinese texts.
    """)
    
    lookup = get_corpus_lookup()
    
    # Search input
    predicate = st.text_input(
        "Enter a predicate (verb/adjective):",
        placeholder="例如：说、发表、担心、热情、有用",
    )
    
    # Common predicates
    st.markdown("**Common predicates to explore:**")
    common = ['说', '进行', '有', '发表', '担心', '热情', '重要', '负责', '了解', '表示']
    cols = st.columns(5)
    for i, pred in enumerate(common):
        with cols[i % 5]:
            if st.button(pred, key=f"common_{pred}"):
                predicate = pred
    
    if predicate:
        show_predicate_info(predicate, lookup)


def show_predicate_info(predicate: str, lookup: CorpusLookup):
    """Show detailed info for a predicate."""
    st.markdown("---")
    
    data = lookup.lookup(predicate)
    
    if not data:
        st.warning(f"'{predicate}' was not found in the corpus.")
        st.markdown("Try a different predicate, or check the spelling.")
        return
    
    total = data.get('total', 0)
    dominant = data.get('dominant_type', '')
    conf = data.get('confidence', 0)
    dominant_name, dominant_chinese = TYPE_NAMES.get(dominant, (dominant, ''))
    
    # Header
    info = CONSTRUCTION_TYPES.get(dominant, {})
    colour = info.get('colour', '#808080')
    
    st.markdown(f"""
    <div style="background: {colour}20; padding: 20px; border-radius: 10px; border-left: 5px solid {colour};">
        <h2 style="margin: 0;">{predicate}</h2>
        <p style="font-size: 1.1em; margin: 10px 0;">
            <strong>{total:,}</strong> instances in the BCC corpus
        </p>
        <p>Most commonly: <strong>{info.get('emoji', '')} {dominant_name}</strong> ({conf*100:.0f}%)</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Distribution
    st.markdown("### Distribution Across Types")
    
    dist = data.get('distribution', {})
    types_data = data.get('types', {})
    
    chart_data = []
    for type_code in ['DA', 'SI', 'MS', 'ABT', 'EVAL', 'DISP']:
        pct = dist.get(type_code, 0)
        count = types_data.get(type_code, 0)
        full_name, chinese = TYPE_NAMES.get(type_code, (type_code, ''))
        chart_data.append({
            'Type': full_name,
            'Percentage': pct,
            'Count': count,
            'Chinese': chinese
        })
    
    df = pd.DataFrame(chart_data)
    
    # Show bar chart
    st.bar_chart(df.set_index('Type')['Percentage'])
    
    # Show table
    display_df = df[df['Percentage'] > 0].copy()
    display_df['Percentage'] = display_df['Percentage'].apply(lambda x: f"{x:.1f}%")
    display_df['Count'] = display_df['Count'].apply(lambda x: f"{x:,}")
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Explanation for dominant type
    st.markdown(f"### Why is '{predicate}' usually {dominant_name}?")
    
    type_exp = TYPE_EXPLANATIONS.get(dominant, {})
    if type_exp:
        st.markdown(f"""
        {type_exp.get('description', '')}
        
        **Test:** {type_exp.get('test', '')}
        
        **Examples:** {', '.join(type_exp.get('examples', []))}
        """)
    
    # Context notes for ambiguous predicates
    if predicate in ['发表', '表示', '有']:
        st.markdown("### ⚠️ Context Matters!")
        
        if predicate == '发表':
            st.markdown("""
            **发表** varies by what follows it:
            - 发表**意见/看法/声明** → **Aboutness** (expressing discourse ABOUT something)
            - 发表**微笑/善意** → **Directed-Action** (directing expression TO someone)
            """)
        elif predicate == '表示':
            st.markdown("""
            **表示** is often Aboutness when expressing a stance:
            - 对此**表示**欢迎/遗憾/关切 → **Aboutness** (expressing stance ABOUT topic)
            - 对他**表示**感谢 → Can be **Directed-Action** if thanking a specific person
            """)
        elif predicate == '有':
            st.markdown("""
            **有** varies greatly by complement:
            - 对...有**兴趣/信心/好感** → **Mental-State** (psychological state)
            - 对...有**益/害/用/帮助** → **Evaluation** (effect FOR someone)
            - 对...有**意见/看法** → **Aboutness** (having opinion ABOUT)
            """)
    
    # Similar predicates
    st.markdown("### Similar Predicates")
    similar = lookup.get_similar_predicates(predicate, limit=8)
    if similar:
        cols = st.columns(4)
        for i, (pred, type_code, count) in enumerate(similar):
            with cols[i % 4]:
                st.markdown(f"**{pred}** ({count:,})")
    else:
        st.markdown("No similar predicates found.")


def show_learning():
    """Learning page with detailed type explanations."""
    st.title("📚 Learn the Six Construction Types")
    
    st.markdown("""
    Understanding these six types will help you use 对 correctly and understand 
    what Chinese sentences mean.
    """)
    
    # Tabs for each type
    tab_labels = [f"{info['emoji']} {info['full_name']}" for info in CONSTRUCTION_TYPES.values()]
    tabs = st.tabs(tab_labels)
    
    for tab, (code, info) in zip(tabs, CONSTRUCTION_TYPES.items()):
        with tab:
            colour = info.get('colour', '#808080')
            
            st.markdown(f"## {info['emoji']} {info['full_name']}")
            st.markdown(f"**Chinese:** {info['chinese_name']}")
            st.markdown(f"**In brief:** {info['short_description']}")
            
            st.markdown("---")
            st.markdown(info.get('description', ''))
            
            # Examples
            st.markdown("### Examples")
            for ch, en in info.get('examples', []):
                st.markdown(f"- **{ch}** — _{en}_")
            
            # Type-specific explanation
            type_exp = TYPE_EXPLANATIONS.get(code, {})
            if type_exp:
                st.markdown("### Quick Test")
                st.info(type_exp.get('test', ''))


def show_statistics():
    """Corpus statistics page."""
    st.title("📊 Corpus Statistics")
    
    st.markdown("""
    These statistics are based on **394,355** instances of 对-constructions 
    from the BCC (Beijing Chinese Corpus).
    """)
    
    # Load frequency data
    freq_file = os.path.join(os.path.dirname(__file__), 'data', 'frequency_data.json')
    
    if os.path.exists(freq_file):
        with open(freq_file, 'r', encoding='utf-8') as f:
            freq_data = json.load(f)
        
        # Overview
        st.markdown("### Distribution by Type")
        
        chart_data = []
        for code in ['DA', 'MS', 'SI', 'EVAL', 'ABT', 'DISP']:
            if code in freq_data:
                data = freq_data[code]
                info = CONSTRUCTION_TYPES.get(code, {})
                chart_data.append({
                    'Type': data.get('full_name', code),
                    'Instances': data.get('count', 0),
                    'Percentage': data.get('percent', 0),
                    'Top Predicate': data.get('top_predicate', ''),
                    'colour': info.get('colour', '#808080')
                })
        
        df = pd.DataFrame(chart_data)
        st.bar_chart(df.set_index('Type')['Percentage'])
        
        # Detailed cards
        st.markdown("### Detailed Breakdown")
        cols = st.columns(3)
        for i, row in df.iterrows():
            with cols[i % 3]:
                st.markdown(f"""
                <div style="background: {row['colour']}20; padding: 15px; 
                            border-radius: 10px; margin: 5px 0;
                            border-left: 4px solid {row['colour']};">
                    <strong>{row['Type']}</strong><br>
                    <span style="font-size: 1.3em;">{row['Instances']:,}</span> instances<br>
                    <span style="color: #666;">{row['Percentage']:.1f}%</span><br>
                    <small>Top: {row['Top Predicate']}</small>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("Frequency data file not found.")


def show_help():
    """Help page."""
    st.title("❓ Help")
    
    st.markdown("### What is 对?")
    st.markdown("""
    **对** (duì) is a Chinese preposition that introduces a noun phrase related 
    to the main action. Depending on context, it can mean "to", "toward", "about", 
    "for", or indicate manner.
    """)
    
    st.markdown("### How do I know which type?")
    st.markdown("""
    Ask these questions:
    
    1. **Is something good/bad/useful FOR Y?** → Evaluation
    2. **Does Y get affected or changed?** → Scoped-Intervention or Directed-Action  
    3. **Is it observable behaviour/manner?** → Disposition
    4. **Does Y trigger a feeling/thought IN X?** → Mental-State
    5. **Does X produce speech/writing ABOUT Y?** → Aboutness
    """)
    
    st.markdown("### Common Confusions")
    
    for key, distinction in KEY_DISTINCTIONS.items():
        with st.expander(f"🔍 {distinction['title']}"):
            st.markdown(distinction['description'])
    
    st.markdown("### About the Data")
    st.markdown("""
    The corpus data comes from the **BCC (Beijing Chinese Corpus)** with 
    **394,355** instances of 对-constructions classified using a hybrid 
    rule-based + machine learning approach (v71).
    
    The classifier achieves approximately **92% accuracy** on held-out test data.
    """)


if __name__ == "__main__":
    main()
