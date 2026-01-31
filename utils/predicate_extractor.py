#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Predicate Extractor (Improved with jieba)
=========================================
Uses jieba for proper Chinese word segmentation to extract
predicates from 对-construction sentences.
"""

import re
from typing import Tuple, Optional, Dict, List

# Try to import jieba, fall back to simple method if not available
try:
    import jieba
    JIEBA_AVAILABLE = True
    # Add custom words to jieba dictionary
    custom_words = [
        '发表', '表态', '置评', '发言', '表示', '提出',
        '担心', '担忧', '害怕', '恐惧', '满意', '不满', '失望',
        '了解', '理解', '认识', '熟悉', '知道', '明白',
        '怀疑', '相信', '信任', '关心', '关注', '注意', '重视',
        '尊重', '尊敬', '喜欢', '讨厌', '热爱', '痛恨',
        '进行', '实行', '实施', '执行', '采取',
        '检查', '监督', '管理', '帮助', '照顾', '保护', '培训',
        '热情', '冷淡', '友好', '客气', '礼貌',
        '有用', '有益', '有害', '有利', '不利',
        '造成', '导致', '带来', '产生',
        '这件事', '那件事', '这个', '那个', '这些', '那些',
    ]
    for word in custom_words:
        jieba.add_word(word)
except ImportError:
    JIEBA_AVAILABLE = False


# Degree adverbs (should be skipped to find the real predicate)
DEGREE_ADVERBS = {
    '很', '非常', '十分', '特别', '比较', '挺', '颇', '极其', 
    '相当', '格外', '更', '更加', '最', '太', '真', '好', '蛮',
    '越来越', '愈来愈', '越发', '尤其', '极', '甚', '颇为',
}

# Negation words (should be included with predicate)
NEGATION_WORDS = {'不', '没', '没有', '未', '非', '莫', '勿', '别', '无'}

# Aspect markers (follow verbs)
ASPECT_MARKERS = {'了', '着', '过', '起来', '下去', '出来'}

# Common predicates by type
PREDICATES = {
    # Mental State (MS) predicates
    'MS': {
        '喜欢', '讨厌', '害怕', '担心', '担忧', '恐惧', '忧虑',
        '满意', '不满', '失望', '绝望', '感激', '感恩', '怨恨', '痛恨',
        '佩服', '敬佩', '钦佩', '崇拜', '景仰', '惊讶', '惊喜', '诧异',
        '气愤', '愤怒', '愤慨', '热爱', '钟爱', '眷恋', '思念',
        '了解', '理解', '认识', '熟悉', '知道', '明白', '懂',
        '怀疑', '相信', '信任', '信赖', '依赖',
        '关心', '关注', '注意', '重视', '在意', '在乎', '留意',
        '尊重', '尊敬', '敬重', '看重', '珍视',
        '感到', '觉得', '感觉',
    },
    # Aboutness (ABT) predicates
    'ABT': {
        '发表', '表态', '置评', '发言', '评价', '评论', '评述', '点评',
        '分析', '研究', '探讨', '考察', '调查', '调研',
        '讨论', '辩论', '争论', '商议', '商讨',
        '报道', '报告', '陈述', '描述', '阐述', '论述',
        '提出', '作出', '做出', '给出', '给予',
    },
    # Scoped Intervention (SI) predicates
    'SI': {
        '进行', '实行', '实施', '执行', '采取', '开展', '展开',
        '检查', '监督', '管理', '整顿', '治理',
        '帮助', '照顾', '保护', '培训', '治疗', '教育',
        '负责', '负', '要求', '施加', '开放',
        '反抗', '抵抗', '对抗', '攻击',
    },
    # Directed Action (DA) predicates
    'DA': {
        '说', '讲', '喊', '叫', '问', '答', '笑', '骂', '吼', '嚷',
        '说道', '问道', '答道', '喊道', '笑道',
        '点头', '摇头', '挥手', '鞠躬', '微笑',
        '解释', '交代', '表示',
    },
    # Disposition (DISP) predicates
    'DISP': {
        '热情', '冷淡', '冷漠', '友好', '友善', '客气', '礼貌', '恭敬',
        '粗暴', '蛮横', '霸道', '好', '坏', '像', '如同',
        '服从', '顺从', '言听计从', '百依百顺',
    },
    # Evaluation (EVAL) predicates
    'EVAL': {
        '有用', '有益', '有害', '有利', '不利', '有效', '无效',
        '重要', '必要', '关键', '危险', '公平', '不公平',
        '造成', '导致', '带来', '产生', '起',
    },
}

# All predicates flat set for quick lookup
ALL_PREDICATES = set()
for preds in PREDICATES.values():
    ALL_PREDICATES.update(preds)


def segment_sentence(sentence: str) -> List[str]:
    """
    Segment a Chinese sentence into words.
    
    Args:
        sentence: Chinese sentence
    
    Returns:
        List of words
    """
    if JIEBA_AVAILABLE:
        return list(jieba.cut(sentence))
    else:
        # Fallback: character-based with some common words
        return _simple_segment(sentence)


def _simple_segment(sentence: str) -> List[str]:
    """Simple segmentation fallback when jieba is not available."""
    # Try to match known words first
    result = []
    i = 0
    while i < len(sentence):
        matched = False
        # Try longer matches first (up to 4 characters)
        for length in range(4, 0, -1):
            if i + length <= len(sentence):
                substr = sentence[i:i+length]
                if substr in ALL_PREDICATES or substr in DEGREE_ADVERBS or substr in NEGATION_WORDS:
                    result.append(substr)
                    i += length
                    matched = True
                    break
        if not matched:
            result.append(sentence[i])
            i += 1
    return result


def extract_dui_parts(sentence: str) -> Dict[str, str]:
    """
    Extract parts of a 对-construction sentence using proper segmentation.
    
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
    
    # Segment the sentence
    words = segment_sentence(sentence)
    
    # Find position of 对
    dui_index = -1
    for i, word in enumerate(words):
        if word == '对':
            dui_index = i
            break
    
    if dui_index == -1:
        # 对 might be part of another word, split manually
        parts = sentence.split('对', 1)
        result['before_dui'] = parts[0]
        if len(parts) > 1:
            result['full_after_dui'] = parts[1]
            # Re-segment the part after 对
            words = segment_sentence(parts[1])
            y_phrase, predicate, after_pred = _extract_y_and_predicate(words)
            result['y_phrase'] = y_phrase
            result['predicate'] = predicate
            result['after_predicate'] = after_pred
        return result
    
    # Get before_dui
    result['before_dui'] = ''.join(words[:dui_index])
    
    # Get after_dui
    after_words = words[dui_index + 1:]
    result['full_after_dui'] = ''.join(after_words)
    
    # Extract Y phrase and predicate
    y_phrase, predicate, after_pred = _extract_y_and_predicate(after_words)
    result['y_phrase'] = y_phrase
    result['predicate'] = predicate
    result['after_predicate'] = after_pred
    
    return result


def _extract_y_and_predicate(words: List[str]) -> Tuple[str, str, str]:
    """
    Extract Y phrase and predicate from words after 对.
    
    Args:
        words: List of segmented words after 对
    
    Returns:
        Tuple of (y_phrase, predicate, after_predicate)
    """
    if not words:
        return '', '', ''
    
    y_parts = []
    predicate = ''
    after_pred_start = 0
    
    i = 0
    while i < len(words):
        word = words[i]
        
        # Skip degree adverbs - they modify the predicate
        if word in DEGREE_ADVERBS:
            # Everything before this is Y phrase
            y_parts = words[:i]
            # Find the predicate after the adverb
            for j in range(i + 1, len(words)):
                if words[j] in ALL_PREDICATES:
                    predicate = words[j]
                    after_pred_start = j + 1
                    break
                elif words[j] not in DEGREE_ADVERBS and words[j] not in NEGATION_WORDS:
                    # Take first non-adverb word as predicate
                    predicate = words[j]
                    after_pred_start = j + 1
                    break
            break
        
        # Check if this word is a predicate
        if word in ALL_PREDICATES:
            y_parts = words[:i]
            predicate = word
            after_pred_start = i + 1
            break
        
        # Check for negation + predicate pattern
        if word in NEGATION_WORDS and i + 1 < len(words):
            next_word = words[i + 1]
            if next_word in ALL_PREDICATES:
                y_parts = words[:i]
                predicate = word + next_word  # Include negation
                after_pred_start = i + 2
                break
        
        i += 1
    
    # If no predicate found, use heuristics
    if not predicate and words:
        # Look for any verb-like word
        for i, word in enumerate(words):
            if len(word) >= 2 and word not in DEGREE_ADVERBS and word not in {'的', '地', '得'}:
                # Check if it could be a predicate (not a common noun ending)
                if not word.endswith(('人', '者', '们', '事', '情')):
                    if i > 0:
                        y_parts = words[:i]
                    predicate = word
                    after_pred_start = i + 1
                    break
        
        # Last resort: first segment is Y, rest is predicate area
        if not predicate and len(words) >= 2:
            y_parts = words[:1]
            predicate = words[1] if words[1] not in DEGREE_ADVERBS else (words[2] if len(words) > 2 else words[1])
            after_pred_start = 2
    
    y_phrase = ''.join(y_parts)
    after_pred = ''.join(words[after_pred_start:]) if after_pred_start < len(words) else ''
    
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
        '他', '她', '我', '你', '您', '咱', '们', '人', '者', '家', '员',
        '师', '生', '民', '众', '客', '友', '敌', '方', '孩子', '老人',
        '同学', '同事', '朋友', '领导', '老师', '学生', '医生', '病人',
    ]
    
    # Inanimate markers
    inanimate_markers = [
        '此', '这', '那', '事', '件', '问题', '情况', '现象', '结果',
        '工作', '任务', '项目', '计划', '政策', '法律', '制度',
        '经济', '社会', '环境', '健康', '身体', '生活', '学习',
        '国家', '世界', '市场', '企业', '公司', '组织',
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
        "我对他的行为非常不满",
        "学生对老师很尊重",
        "这对经济发展有利",
    ]
    
    print("Predicate Extraction Test:")
    print("=" * 60)
    print(f"Jieba available: {JIEBA_AVAILABLE}")
    print("=" * 60)
    
    for sentence in test_sentences:
        parts = extract_dui_parts(sentence)
        animacy = guess_y_animacy(parts['y_phrase'])
        print(f"\n{sentence}")
        print(f"  Y phrase: '{parts['y_phrase']}' ({animacy})")
        print(f"  Predicate: '{parts['predicate']}'")
        print(f"  After predicate: '{parts['after_predicate']}'")
