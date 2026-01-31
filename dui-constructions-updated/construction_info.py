#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Construction Type Information
=============================
Full names, descriptions, and examples for each 对-construction type.
User-friendly content for display in the Streamlit app.
"""

# Construction type definitions with full names (no acronyms in display)
CONSTRUCTION_TYPES = {
    'DA': {
        'code': 'DA',
        'full_name': 'Directed-Action',
        'chinese_name': '指向动作',
        'short_description': 'Action directed TO someone',
        'description': '''
**Directed-Action** constructions describe an action that is intentionally 
directed **toward** a person or recipient. The action flows TO or AT the 
target, who receives it but is not necessarily transformed by it.

**Key characteristics:**
- The action has inherent direction toward Y
- Y is typically a person or animate being
- Common with speech acts and gestures
- X is doing something TO Y

**Diagnostic question:** Is X doing something TO/AT Y?
''',
        'examples': [
            ('他对我说了几句话', 'He said a few words TO me'),
            ('她对观众鞠躬', 'She bowed TO the audience'),
            ('老师对学生点头', 'The teacher nodded TO the student'),
            ('他对她微笑', 'He smiled AT her'),
            ('妈妈对孩子喊', 'Mother called TO the child'),
        ],
        'typical_verbs': ['说', '讲', '喊', '叫', '问', '答', '笑', '点头', '挥手', '鞠躬'],
        'colour': '#FF6B6B',
        'emoji': '➡️'
    },
    
    'SI': {
        'code': 'SI',
        'full_name': 'Scoped-Intervention',
        'chinese_name': '范围干预',
        'short_description': 'Intervention ON a scope or domain',
        'description': '''
**Scoped-Intervention** constructions describe a bounded, procedural 
intervention **upon** Y. Y is treated as a domain, scope, or patient 
under X's operational control and undergoes some change or effect.

**Key characteristics:**
- Y is a bounded operational domain
- Y undergoes change or is affected
- Often involves institutional or formal actions
- X intervenes UPON Y

**Diagnostic question:** Is X intervening ON/UPON Y's scope?
''',
        'examples': [
            ('政府对企业进行检查', 'The government conducts inspections ON enterprises'),
            ('警方对嫌疑人采取行动', 'Police take action ON the suspect'),
            ('医生对病人进行治疗', 'The doctor provides treatment TO the patient'),
            ('学校对学生进行培训', 'The school provides training TO students'),
            ('法院对案件进行审理', 'The court conducts trial ON the case'),
        ],
        'typical_verbs': ['进行', '实行', '实施', '执行', '采取', '检查', '监督', '管理', '帮助', '保护'],
        'colour': '#4ECDC4',
        'emoji': '🔧'
    },
    
    'MS': {
        'code': 'MS',
        'full_name': 'Mental-State',
        'chinese_name': '心理状态',
        'short_description': 'Internal psychological state triggered by Y',
        'description': '''
**Mental-State** constructions describe an internal psychological, emotional, 
or cognitive state where Y serves as the **stimulus** that triggers the state 
in X. Y causes or elicits the psychological response.

**Key characteristics:**
- Describes internal states (not directly observable)
- Y triggers the psychological response in X
- Includes emotions, cognition, and attitudes
- Y is not affected by X's state

**Diagnostic question:** Does Y trigger X's internal psychological state?
''',
        'examples': [
            ('我对这件事很担心', 'I am very worried ABOUT this matter'),
            ('他对音乐很感兴趣', 'He is very interested IN music'),
            ('她对他很尊重', 'She respects him greatly'),
            ('我对结果很满意', 'I am satisfied WITH the result'),
            ('他们对未来充满信心', 'They are confident ABOUT the future'),
        ],
        'typical_verbs': ['喜欢', '担心', '害怕', '满意', '了解', '理解', '尊重', '关心', '信任', '怀疑'],
        'colour': '#95E1D3',
        'emoji': '💭'
    },
    
    'ABT': {
        'code': 'ABT',
        'full_name': 'Aboutness',
        'chinese_name': '论题关涉',
        'short_description': 'Discourse or commentary ABOUT Y',
        'description': '''
**Aboutness** constructions describe external cognitive or discursive 
activity **about** Y. Y is the topic, subject matter, or content of X's 
discourse. X produces speech, writing, or commentary about Y.

**Key characteristics:**
- External activity (observable)
- Y is the topic of discourse
- Y is not affected by the discourse
- X produces output about Y

**Diagnostic question:** Does X produce discourse ABOUT Y?
''',
        'examples': [
            ('专家对此发表意见', 'Experts express opinions ABOUT this'),
            ('记者对事件进行报道', 'Journalists report ON the event'),
            ('学者对问题进行分析', 'Scholars analyse the problem'),
            ('委员会对提案进行讨论', 'The committee discusses the proposal'),
            ('他对此不予置评', 'He declined to comment ON this'),
        ],
        'typical_verbs': ['发表', '评价', '评论', '分析', '研究', '讨论', '报道', '调查', '表态', '置评'],
        'colour': '#F38181',
        'emoji': '💬'
    },
    
    'DISP': {
        'code': 'DISP',
        'full_name': 'Disposition',
        'chinese_name': '态度行为',
        'short_description': 'Behavioural manner TOWARD someone',
        'description': '''
**Disposition** constructions describe a characteristic behavioural manner 
or social attitude **toward** Y in interpersonal interaction. This describes 
HOW X behaves or treats Y in observable social ways.

**Key characteristics:**
- Observable behavioural manner
- Describes how X treats/relates to Y
- Focus on style or manner of interaction
- Y typically experiences X's manner

**Diagnostic question:** Is X treating Y in a particular manner?
''',
        'examples': [
            ('她对客人很热情', 'She is very warm TOWARD the guests'),
            ('他对同事很冷淡', 'He is cold TOWARD his colleagues'),
            ('父母对孩子像朋友一样', 'Parents treat children LIKE friends'),
            ('老板对员工很客气', 'The boss is polite TOWARD employees'),
            ('他对人总是很友好', 'He is always friendly TOWARD people'),
        ],
        'typical_verbs': ['热情', '冷淡', '友好', '客气', '礼貌', '粗暴', '好', '像'],
        'colour': '#AA96DA',
        'emoji': '🤝'
    },
    
    'EVAL': {
        'code': 'EVAL',
        'full_name': 'Evaluation',
        'chinese_name': '评价效果',
        'short_description': 'Good/bad/useful FOR Y',
        'description': '''
**Evaluation** constructions describe X being evaluated as good, bad, useful, 
or harmful **for** Y. 对 introduces the perspective, beneficiary, or frame 
of reference from which X is judged.

**Key characteristics:**
- X has a property relative to Y
- Y is the perspective or beneficiary
- X is what is being evaluated (not agent)
- Often involves benefit or harm to Y

**Diagnostic question:** Is X good/bad/useful FOR Y?
''',
        'examples': [
            ('运动对健康有益', 'Exercise is beneficial FOR health'),
            ('这对学生很重要', 'This is important FOR students'),
            ('吸烟对身体有害', 'Smoking is harmful FOR the body'),
            ('这个方法对初学者很有效', 'This method is effective FOR beginners'),
            ('新政策对经济有利', 'The new policy is beneficial FOR the economy'),
        ],
        'typical_verbs': ['有用', '有益', '有害', '重要', '必要', '有效', '公平', '有利', '不利'],
        'colour': '#FCBAD3',
        'emoji': '⚖️'
    }
}


def get_type_info(code: str) -> dict:
    """Get information for a construction type by code."""
    return CONSTRUCTION_TYPES.get(code, {})


def get_full_name(code: str) -> str:
    """Get full name for a construction type code."""
    info = CONSTRUCTION_TYPES.get(code, {})
    return info.get('full_name', code)


def get_chinese_name(code: str) -> str:
    """Get Chinese name for a construction type code."""
    info = CONSTRUCTION_TYPES.get(code, {})
    return info.get('chinese_name', '')


def get_all_types() -> dict:
    """Get all construction type definitions."""
    return CONSTRUCTION_TYPES


def format_type_display(code: str, include_emoji: bool = True) -> str:
    """Format a construction type for display."""
    info = CONSTRUCTION_TYPES.get(code, {})
    if not info:
        return code
    
    emoji = info.get('emoji', '') + ' ' if include_emoji else ''
    return f"{emoji}{info['full_name']} ({info['chinese_name']})"


# Comparison data for the comparison page
COMPARISON_TABLE = [
    {
        'Type': 'Directed-Action',
        'Chinese': '指向动作',
        'Key Feature': 'Action directed TO Y',
        "Y's Role": 'Recipient (receives action)',
        "X's Role": 'Agent/Speaker',
        'Y Affected?': 'Mildly (receives)'
    },
    {
        'Type': 'Scoped-Intervention',
        'Chinese': '范围干预',
        'Key Feature': 'Intervention ON Y',
        "Y's Role": 'Scope/Patient (affected)',
        "X's Role": 'Agent/Authority',
        'Y Affected?': 'Yes (changes)'
    },
    {
        'Type': 'Mental-State',
        'Chinese': '心理状态',
        'Key Feature': 'Y triggers state in X',
        "Y's Role": 'Stimulus (triggers state)',
        "X's Role": 'Experiencer',
        'Y Affected?': 'No'
    },
    {
        'Type': 'Aboutness',
        'Chinese': '论题关涉',
        'Key Feature': 'Discourse ABOUT Y',
        "Y's Role": 'Topic (discussed)',
        "X's Role": 'Communicator',
        'Y Affected?': 'No'
    },
    {
        'Type': 'Disposition',
        'Chinese': '态度行为',
        'Key Feature': 'Manner TOWARD Y',
        "Y's Role": 'Target (of manner)',
        "X's Role": 'Actor',
        'Y Affected?': 'No (experiences)'
    },
    {
        'Type': 'Evaluation',
        'Chinese': '评价效果',
        'Key Feature': 'Good/bad FOR Y',
        "Y's Role": 'Beneficiary/Perspective',
        "X's Role": 'Theme (evaluated)',
        'Y Affected?': 'Benefits/suffers'
    }
]


# Key distinctions for help page
KEY_DISTINCTIONS = {
    'MS_vs_ABT': {
        'title': 'Mental-State vs Aboutness',
        'description': '''
This is often the trickiest distinction:

**Mental-State**: Y triggers an internal state IN X
- Example: 对他很了解 (understand him — internal knowledge)
- The verb describes what happens inside X's mind

**Aboutness**: X produces discourse ABOUT Y
- Example: 对此发表意见 (express opinions about this — external speech)
- X creates observable output (speech, writing, analysis)

**Quick test:** Does X produce observable output? If yes → Aboutness
''',
    },
    'DA_vs_SI': {
        'title': 'Directed-Action vs Scoped-Intervention',
        'description': '''
Both involve action toward Y, but:

**Directed-Action**: Y receives action, unchanged
- Example: 对他说话 (speak TO him)
- The verb cannot take Y as direct object: 说他 ✗

**Scoped-Intervention**: Y is affected/changed
- Example: 对他进行治疗 (provide treatment TO him)
- The verb can take Y as direct object: 帮助他 ✓

**Quick test:** Is Y affected or changed? If yes → Scoped-Intervention
''',
    },
    'DISP_vs_MS': {
        'title': 'Disposition vs Mental-State',
        'description': '''
**Disposition**: Observable behavioural manner
- Example: 对他很热情 (warm toward him — you can see the behaviour)
- Describes HOW X acts

**Mental-State**: Internal psychological state
- Example: 对他很尊重 (respect him — internal feeling)
- Describes what X feels/thinks inside

**Quick test:** Can you observe it directly? If yes → Disposition
''',
    }
}
