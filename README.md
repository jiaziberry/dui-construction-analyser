# Chinese 对-Construction Analyser

A user-friendly web application for analysing Chinese sentences containing 对 (duì) 
and identifying which of six grammatical construction types is being used.

## Features

- **Sentence Analysis**: Enter any Chinese sentence with 对 and get instant classification with explanation
- **Learn the Six Types**: Detailed explanations of all construction types with examples
- **Compare Types**: Side-by-side comparison to understand key differences
- **Frequency Data**: Corpus-based distribution statistics
- **Help & FAQ**: Common questions and guidance for tricky distinctions

## The Six Construction Types

| Type | Chinese | Brief Description | Example |
|------|---------|-------------------|---------|
| **Directed-Action** | 指向动作 | Action directed TO someone | 他对我说了几句话 |
| **Scoped-Intervention** | 范围干预 | Intervention ON a scope | 政府对企业进行检查 |
| **Mental-State** | 心理状态 | Internal state triggered by Y | 我对这件事很担心 |
| **Aboutness** | 论题关涉 | Discourse ABOUT Y | 专家对此发表意见 |
| **Disposition** | 态度行为 | Behavioural manner TOWARD Y | 她对客人很热情 |
| **Evaluation** | 评价效果 | Good/bad/useful FOR Y | 运动对健康有益 |

## Installation

### Basic Installation (Simple Classifier)

```bash
pip install streamlit pandas
streamlit run app.py
```

### Full Installation (With v70/v71 Classifier)

For the full classifier with 1,400+ linguistic rules:

```bash
pip install -r requirements.txt
streamlit run app.py
```

Ensure `dui_classifier_v70.py` and optionally `dui_classifier_v71.py` are in the same directory.

## Project Structure

```
dui-construction-app/
├── app.py                    # Main Streamlit application
├── dui_classifier_v70.py     # Rule-based classifier (1,400+ rules)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── data/
│   └── frequency_data.json   # Corpus frequency statistics
└── utils/
    ├── __init__.py           # Package initialisation
    ├── classifier.py         # Classifier wrapper
    ├── construction_info.py  # Type definitions and descriptions
    ├── predicate_extractor.py # Predicate extraction utilities
    └── predicate_lookup.py   # Corpus-based predicate lookup
```

**Note:** The v71 hybrid classifier (with BERT) is NOT needed for the web app.
The web app uses only the v70 rule-based classifier for fast, accurate classification.

## Quick Start

1. **Clone or download** the repository
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Run the app**: `streamlit run app.py`
4. **Open browser** to `http://localhost:8501`

## Example Classifications

| Sentence | Type | Why |
|----------|------|-----|
| 专家对此发表意见 | Aboutness | Experts produce discourse (opinions) ABOUT the topic |
| 他对我说了几句话 | Directed-Action | Speech directed TO a person |
| 政府对企业进行检查 | Scoped-Intervention | Government intervenes ON enterprises |
| 我对这件事很担心 | Mental-State | Worry is an internal psychological state |
| 她对客人很热情 | Disposition | Warmth is observable behavioural manner |
| 运动对健康有益 | Evaluation | Exercise is evaluated as beneficial FOR health |

## Key Distinctions

### Mental-State vs Aboutness

This is the trickiest distinction:

- **Mental-State**: Y triggers an internal state IN X (not observable)
  - Example: 对他很了解 (understand him — internal knowledge)
  
- **Aboutness**: X produces discourse ABOUT Y (observable output)
  - Example: 对此发表意见 (express opinions — external speech)

**Test**: Does X produce observable output? If yes → Aboutness

### Directed-Action vs Scoped-Intervention

- **Directed-Action**: Y receives action but is unchanged
  - Test: 说他 ✗ (verb cannot take direct object)
  
- **Scoped-Intervention**: Y is affected or changed
  - Test: 帮助他 ✓ (verb can take direct object)

## Version History

- **v70.1** (January 2026): 
  - Added 发表, 表态, 置评, 发言, 评价, 评论 to high-priority discourse verbs
  - Fixed: "专家对此发表意见" now correctly classified as Aboutness (was incorrectly Directed-Action)

## Technical Details

The classifier uses over 1,400 linguistic rules developed through analysis of:
- **BCC Corpus**: 394,355 instances of 对-constructions
- **Validation data**: 92% accuracy on held-out test set

The theoretical framework is based on Usage-Based Construction Grammar, distinguishing 
constructions by semantic roles, argument structure, and the relationship between 
X (subject), Y (对-phrase), and the predicate.

## For Developers

### Using the Classifier Programmatically

```python
from utils.classifier import DuiClassifier

classifier = DuiClassifier()
result = classifier.classify("专家对此发表意见")

print(result['full_name'])     # "Aboutness"
print(result['confidence'])    # 0.92
print(result['explanation'])   # "Contains discourse verb..."
```

### Adding New Rules

To add new classification rules, edit `dui_classifier_v70.py` and add entries to the 
appropriate verb/pattern sets (e.g., `discourse_predicates_high_priority`).

## Credits

Developed as part of doctoral research on Chinese 对-constructions using 
Usage-Based Construction Grammar principles.

## Licence

MIT Licence
