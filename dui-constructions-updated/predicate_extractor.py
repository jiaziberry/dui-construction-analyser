#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Predicate Extractor
===================
Utility for extracting predicates and related information from
Chinese sentences containing 对-constructions.
"""

import re
from typing import Tuple, Optional, Dict


def extract_dui_parts(sentence: str) -> Dict[str, str]:
    """
    Extract parts of a 对-construction sentence.
    
    Args:
        sentence: Chinese sentence containing 对
    
    Returns:
        Dictionary with:
            - before_dui: Text before 对
            - y_phrase: The Y phrase (object of 对)
            - predicate: Main predicate/verb
            - after_predicate: Text after predicate
            - full_after_dui: Everything after 对
    """
    result = {
        'before_dui': '',
        'y_phrase': '',
        'predicate': '',
        'after_predicate': '',
        'full_after_dui': ''
    }
    
    if '对' not in sentence:
        return result
    
    parts = sentence.split('对', 1)
    result['before_dui'] = parts[0]
    
    if len(parts) < 2:
        return result
    
    after_dui = parts[1]
    result['full_after_dui'] = after_dui
    
    # Extract Y phrase and predicate
    # Y phrase is typically 1-6 characters before the main verb
    y_phrase, predicate, after_pred = _split_y_and_predicate(after_dui)
    
    result['y_phrase'] = y_phrase
    result['predicate'] = predicate
    result['after_predicate'] = after_pred
    
    return result


def _split_y_and_predicate(after_dui: str) -> Tuple[str, str, str]:
    """
    Split the text after 对 into Y phrase and predicate.
    
    Args:
        after_dui: Text after 对
    
    Returns:
        Tuple of (y_phrase, predicate, after_predicate)
    """
    # Common patterns to identify where predicate starts
    # Degree adverbs that precede predicates
    degree_adverbs = ['很', '非常', '十分', '特别', '比较', '挺', '颇', '极其', '相当', '格外']
    
    # Common verb/adjective starters
    verb_starters = [
        # Discourse verbs
        '发表', '表态', '置评', '发言', '表示', '提出', '采访', '调查',
        '研究', '分析', '探讨', '讨论', '评价', '评论', '评估',
        '报道', '陈述', '进行', '实行', '实施', '执行', '采取',
        # Mental state verbs
        '喜欢', '讨厌', '害怕', '担心', '满意', '不满', '失望',
        '了解', '理解', '认识', '熟悉', '知道', '明白',
        '怀疑', '相信', '信任', '关心', '关注', '注意', '重视',
        '尊重', '尊敬', '感到', '觉得',
        # Intervention verbs
        '检查', '监督', '管理', '帮助', '照顾', '保护', '培训', '治疗',
        # Speech verbs
        '说', '讲', '喊', '叫', '问', '答', '笑', '点头', '挥手',
        # Disposition words
        '热情', '冷淡', '友好', '客气', '礼貌', '好', '像',
        # Evaluation words
        '有用', '有益', '有害', '重要', '必要', '有效', '公平',
        '有利', '不利', '造成', '导致', '带来',
    ]
    
    # Try to find where predicate starts
    y_end = 0
    predicate_start = 0
    
    # First, check for degree adverbs
    for i, char in enumerate(after_dui):
        found_adverb = False
        for adv in degree_adverbs:
            if after_dui[i:].startswith(adv):
                predicate_start = i
                y_end = i
                found_adverb = True
                break
        if found_adverb:
            break
        
        # Check for verb starters
        for verb in verb_starters:
            if after_dui[i:].startswith(verb):
                predicate_start = i
                y_end = i
                break
        else:
            continue
        break
    
    # If no verb found, use heuristic: Y is first 2-4 chars
    if predicate_start == 0:
        # Look for common Y endings
        for i in range(min(6, len(after_dui)), 0, -1):
            potential_y = after_dui[:i]
            # Y typically ends with: 此, 他, 她, 它, 这, 那, 人, etc.
            if potential_y.endswith(('此', '他', '她', '它', '这', '那', '人', '们', '者')):
                y_end = i
                predicate_start = i
                break
        
        # Default: assume Y is first 2 characters
        if y_end == 0:
            y_end = min(2, len(after_dui))
            predicate_start = y_end
    
    y_phrase = after_dui[:y_end].strip()
    remaining = after_dui[predicate_start:].strip()
    
    # Extract predicate (usually 2-4 characters)
    predicate = ''
    after_pred = remaining
    
    for verb in verb_starters:
        if remaining.startswith(verb):
            predicate = verb
            after_pred = remaining[len(verb):]
            break
    
    if not predicate and remaining:
        # Take first 2 characters as predicate
        predicate = remaining[:2] if len(remaining) >= 2 else remaining
        after_pred = remaining[len(predicate):]
    
    return y_phrase, predicate, after_pred


def extract_predicate(sentence: str) -> str:
    """
    Extract the main predicate from a 对-construction sentence.
    
    Args:
        sentence: Chinese sentence containing 对
    
    Returns:
        Extracted predicate string
    """
    parts = extract_dui_parts(sentence)
    return parts.get('predicate', '')


def extract_y_phrase(sentence: str) -> str:
    """
    Extract the Y phrase (object of 对) from a sentence.
    
    Args:
        sentence: Chinese sentence containing 对
    
    Returns:
        Extracted Y phrase
    """
    parts = extract_dui_parts(sentence)
    return parts.get('y_phrase', '')


def guess_y_animacy(y_phrase: str) -> str:
    """
    Guess the animacy of the Y phrase.
    
    Args:
        y_phrase: The Y phrase to analyse
    
    Returns:
        'animate', 'inanimate', or 'unknown'
    """
    # Animate markers
    animate_markers = [
        '他', '她', '我', '你', '们', '人', '者', '家', '员',
        '师', '生', '民', '众', '客', '友', '敌', '方',
    ]
    
    # Inanimate markers
    inanimate_markers = [
        '此', '这', '那', '事', '件', '问题', '情况', '现象',
        '工作', '任务', '项目', '计划', '政策', '法律',
        '经济', '社会', '环境', '健康', '身体',
    ]
    
    for marker in animate_markers:
        if marker in y_phrase:
            return 'animate'
    
    for marker in inanimate_markers:
        if marker in y_phrase:
            return 'inanimate'
    
    return 'unknown'


if __name__ == "__main__":
    # Test extraction
    test_sentences = [
        "专家对此发表意见",
        "他对我说了几句话",
        "政府对企业进行检查",
        "我对这件事很担心",
        "她对客人很热情",
        "运动对健康有益",
    ]
    
    print("Predicate Extraction Test:")
    print("=" * 60)
    for sentence in test_sentences:
        parts = extract_dui_parts(sentence)
        animacy = guess_y_animacy(parts['y_phrase'])
        print(f"\n{sentence}")
        print(f"  Y phrase: {parts['y_phrase']} ({animacy})")
        print(f"  Predicate: {parts['predicate']}")
        print(f"  After predicate: {parts['after_predicate']}")
