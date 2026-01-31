#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Predicate Extractor (Improved with jieba)
=========================================
Uses jieba for proper Chinese word segmentation to extract
predicates from 对-construction sentences.

Key improvements:
- Forces split on 对 before segmentation
- Adds common predicates to jieba dictionary
- Handles cases where jieba combines predicate+complement
"""

import re
from typing import Tuple, Optional, Dict, List

# Try to import jieba
try:
    import jieba
    JIEBA_AVAILABLE = True
    
    # Add common predicates to ensure they're segmented correctly
    PREDICATE_WORDS = [
        # Mental State (MS)
        '喜欢', '讨厌', '害怕', '担心', '担忧', '恐惧', '忧虑',
        '满意', '不满', '失望', '绝望', '感激', '感恩', '怨恨', '痛恨',
        '佩服', '敬佩', '钦佩', '崇拜', '景仰', '惊讶', '惊喜', '诧异',
        '气愤', '愤怒', '愤慨', '热爱', '钟爱', '眷恋', '思念',
        '了解', '理解', '认识', '熟悉', '知道', '明白', '懂',
        '怀疑', '相信', '信任', '信赖', '依赖',
        '关心', '关注', '注意', '重视', '在意', '在乎', '留意',
        '尊重', '尊敬', '敬重', '看重', '珍视',
        '感到', '觉得', '感觉',
        # MS - Interest/attitude predicates (很重要!)
        '感兴趣', '有兴趣', '没兴趣', '没有兴趣', '不感兴趣',
        '有好感', '有信心', '有把握', '有印象', '没印象',
        '有意见', '有看法', '抱有', '怀有', '持有',
        # Aboutness (ABT)
        '发表', '表态', '置评', '发言', '评价', '评论', '评述', '点评',
        '分析', '研究', '探讨', '考察', '调查', '调研',
        '讨论', '辩论', '争论', '商议', '商讨',
        '报道', '报告', '陈述', '描述', '阐述', '论述',
        '提出', '作出', '做出', '给出', '给予',
        # Scoped Intervention (SI)
        '进行', '实行', '实施', '执行', '采取', '开展', '展开',
        '检查', '监督', '管理', '整顿', '治理',
        '帮助', '照顾', '保护', '培训', '治疗', '教育',
        '负责', '负', '要求', '施加', '开放',
        '反抗', '抵抗', '对抗', '攻击',
        # Directed Action (DA)
        '说', '讲', '喊', '叫', '问', '答', '笑', '骂', '吼', '嚷',
        '说道', '问道', '答道', '喊道', '笑道',
        '点头', '摇头', '挥手', '鞠躬', '微笑',
        '解释', '交代', '表示',
        # Disposition (DISP)
        '热情', '冷淡', '冷漠', '友好', '友善', '客气', '礼貌', '恭敬',
        '粗暴', '蛮横', '霸道', '好', '坏', '像', '如同',
        '服从', '顺从', '言听计从', '百依百顺',
        # Evaluation (EVAL)
        '有用', '有益', '有害', '有利', '不利', '有效', '无效',
        '重要', '必要', '关键', '危险', '公平', '不公平',
        '造成', '导致', '带来', '产生', '起',
    ]
    
    # Common complements that should NOT be part of predicates
    COMPLEMENTS = [
        '意见', '看法', '观点', '声明', '讲话', '评论', '建议',
        '影响', '作用', '效果', '贡献', '帮助', '支持', '反对',
        '兴趣', '信心', '好感', '印象', '了解', '认识',
        '检查', '调查', '研究', '分析', '治疗', '培训',
    ]
    
    # Common nouns that should NOT be split
    COMMON_NOUNS = [
        '问题', '情况', '现象', '事情', '事件', '结果', '原因',
        '这个', '那个', '这些', '那些', '这件事', '那件事',
        '工作', '学习', '生活', '健康', '经济', '社会', '环境',
        '企业', '公司', '政府', '国家', '世界', '市场',
        '老师', '学生', '朋友', '同事', '领导', '客人',
        '经济发展', '社会发展', '科学技术',
    ]
    
    for word in COMMON_NOUNS:
        jieba.add_word(word, freq=100000)
    
    # Add all predicate words with high frequency to force segmentation
    for word in PREDICATE_WORDS:
        jieba.add_word(word, freq=100000)
    
    # Add complements separately
    for word in COMPLEMENTS:
        jieba.add_word(word, freq=90000)
    
except ImportError:
    JIEBA_AVAILABLE = False
    PREDICATE_WORDS = []


# Degree adverbs (should be skipped to find the real predicate)
DEGREE_ADVERBS = {
    '很', '非常', '十分', '特别', '比较', '挺', '颇', '极其', 
    '相当', '格外', '更', '更加', '最', '太', '真', '好', '蛮',
    '越来越', '愈来愈', '越发', '尤其', '极', '甚', '颇为',
}

# Negation words
NEGATION_WORDS = {'不', '没', '没有', '未', '非', '莫', '勿', '别', '无'}

# Common nouns - these should NEVER be treated as predicates
COMMON_NOUNS = {
    '问题', '情况', '现象', '事情', '事件', '结果', '原因',
    '这个', '那个', '这些', '那些', '这件事', '那件事',
    '工作', '学习', '生活', '健康', '经济', '社会', '环境',
    '企业', '公司', '政府', '国家', '世界', '市场',
    '老师', '学生', '朋友', '同事', '领导', '客人',
    '经济发展', '社会发展', '科学技术', '意见', '看法',
}

# All predicates as a set for quick lookup
ALL_PREDICATES = set(PREDICATE_WORDS) if PREDICATE_WORDS else set()


def segment_sentence(text: str) -> List[str]:
    """
    Segment Chinese text into words.
    """
    if JIEBA_AVAILABLE:
        return list(jieba.cut(text))
    else:
        return _simple_segment(text)


def _simple_segment(text: str) -> List[str]:
    """Simple segmentation fallback."""
    result = []
    i = 0
    while i < len(text):
        matched = False
        for length in range(4, 0, -1):
            if i + length <= len(text):
                substr = text[i:i+length]
                if substr in ALL_PREDICATES or substr in DEGREE_ADVERBS:
                    result.append(substr)
                    i += length
                    matched = True
                    break
        if not matched:
            result.append(text[i])
            i += 1
    return result


def extract_dui_parts(sentence: str) -> Dict[str, str]:
    """
    Extract parts of a 对-construction sentence.
    
    Returns:
        Dictionary with before_dui, y_phrase, predicate, after_predicate, full_after_dui
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
    
    # CRITICAL: Split on 对 FIRST, then segment each part
    # This avoids jieba combining 对 with following characters (e.g., 对此)
    parts = sentence.split('对', 1)
    result['before_dui'] = parts[0]
    
    if len(parts) < 2:
        return result
    
    after_dui = parts[1]
    result['full_after_dui'] = after_dui
    
    # Now segment the part after 对
    words = segment_sentence(after_dui)
    
    # Extract Y phrase and predicate
    y_phrase, predicate, after_pred = _extract_y_and_predicate(words, after_dui)
    
    result['y_phrase'] = y_phrase
    result['predicate'] = predicate
    result['after_predicate'] = after_pred
    
    return result


def _find_predicate_in_word(word: str) -> Optional[str]:
    """
    Check if a word contains a known predicate (for cases where jieba combined them).
    E.g., "发表意见" should return "发表"
    E.g., "不感兴趣" should return "不感兴趣" or "感兴趣"
    
    Returns None if:
    - word is a common noun (e.g., "问题" should not return "问")
    - no predicate found
    """
    # CRITICAL: Skip common nouns entirely - don't try to extract predicates from them
    if word in COMMON_NOUNS:
        return None
    
    # First check if it's already a known predicate
    if word in ALL_PREDICATES:
        return word
    
    # Check for negation prefix (不/没/未) + predicate
    # E.g., "不感兴趣" → return "不感兴趣" (keep negation)
    if word.startswith(('不', '没', '未')):
        remainder = word[1:]
        # Check if remainder is a predicate
        if remainder in ALL_PREDICATES:
            return word  # Return with negation: "不感兴趣"
        # Check if remainder starts with a predicate
        for pred in sorted(ALL_PREDICATES, key=len, reverse=True):
            if remainder.startswith(pred):
                return word[:1] + pred  # Return negation + predicate
    
    # Check if any known predicate is at the START of this word
    for pred in sorted(ALL_PREDICATES, key=len, reverse=True):  # Longer predicates first
        if word.startswith(pred) and len(word) > len(pred):
            # Make sure the remaining part isn't making this a different word
            remaining = word[len(pred):]
            # Don't split if this creates a nonsense split
            if remaining and remaining[0] not in '的地得了着过':
                # Check if the full word might be a noun
                if word not in COMMON_NOUNS:
                    return pred
    
    return None


def _extract_y_and_predicate(words: List[str], original_text: str) -> Tuple[str, str, str]:
    """
    Extract Y phrase and predicate from words after 对.
    """
    if not words:
        return '', '', ''
    
    y_parts = []
    predicate = ''
    after_pred = ''
    
    i = 0
    while i < len(words):
        word = words[i]
        
        # Skip degree adverbs - they precede the predicate
        if word in DEGREE_ADVERBS:
            y_parts = words[:i]
            # Look for predicate after adverb
            for j in range(i + 1, len(words)):
                candidate = words[j]
                # Check if this word contains a predicate
                found_pred = _find_predicate_in_word(candidate)
                if found_pred:
                    predicate = found_pred
                    # After predicate is the rest
                    remaining_of_word = candidate[len(found_pred):]
                    after_parts = [remaining_of_word] if remaining_of_word else []
                    after_parts.extend(words[j+1:])
                    after_pred = ''.join(after_parts)
                    break
                elif candidate not in DEGREE_ADVERBS and candidate not in NEGATION_WORDS:
                    predicate = candidate
                    after_pred = ''.join(words[j+1:])
                    break
            break
        
        # Check if this word IS or CONTAINS a predicate
        found_pred = _find_predicate_in_word(word)
        if found_pred:
            y_parts = words[:i]
            predicate = found_pred
            # The rest of this word (if any) plus following words
            remaining_of_word = word[len(found_pred):]
            after_parts = [remaining_of_word] if remaining_of_word else []
            after_parts.extend(words[i+1:])
            after_pred = ''.join(after_parts)
            break
        
        # Check for negation + predicate pattern
        if word in NEGATION_WORDS and i + 1 < len(words):
            next_word = words[i + 1]
            found_pred = _find_predicate_in_word(next_word)
            if found_pred:
                y_parts = words[:i]
                predicate = word + found_pred  # Include negation
                remaining_of_word = next_word[len(found_pred):]
                after_parts = [remaining_of_word] if remaining_of_word else []
                after_parts.extend(words[i+2:])
                after_pred = ''.join(after_parts)
                break
        
        i += 1
    
    # If no predicate found, use fallback
    if not predicate and words:
        # Try to find any 2-character verb-like word
        for idx, word in enumerate(words):
            if len(word) >= 2 and word not in DEGREE_ADVERBS and word not in {'的', '地', '得'}:
                if not word.endswith(('人', '者', '们')):
                    y_parts = words[:idx] if idx > 0 else []
                    predicate = word
                    after_pred = ''.join(words[idx+1:])
                    break
    
    y_phrase = ''.join(y_parts)
    
    return y_phrase, predicate, after_pred


def extract_predicate(sentence: str) -> str:
    """Extract the main predicate from a 对-construction sentence."""
    parts = extract_dui_parts(sentence)
    return parts.get('predicate', '')


def extract_y_phrase(sentence: str) -> str:
    """Extract the Y phrase (object of 对) from a sentence."""
    parts = extract_dui_parts(sentence)
    return parts.get('y_phrase', '')


def guess_y_animacy(y_phrase: str) -> str:
    """Guess the animacy of the Y phrase."""
    animate_markers = [
        '他', '她', '我', '你', '您', '咱', '们', '人', '者', '家', '员',
        '师', '生', '民', '众', '客', '友', '敌', '方', '孩子', '老人',
        '同学', '同事', '朋友', '领导', '老师', '学生', '医生', '病人',
    ]
    
    inanimate_markers = [
        '此', '这', '那', '事', '件', '问题', '情况', '现象', '结果',
        '工作', '任务', '项目', '计划', '政策', '法律', '制度',
        '经济', '社会', '环境', '健康', '身体', '生活', '学习',
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
        "我们对这个问题进行了深入研究",
    ]
    
    print("Predicate Extraction Test:")
    print("=" * 60)
    print(f"Jieba available: {JIEBA_AVAILABLE}")
    print("=" * 60)
    
    for sentence in test_sentences:
        parts = extract_dui_parts(sentence)
        animacy = guess_y_animacy(parts['y_phrase'])
        print(f"\n{sentence}")
        print(f"  Y: '{parts['y_phrase']}' ({animacy})")
        print(f"  Predicate: '{parts['predicate']}'")
        print(f"  After: '{parts['after_predicate']}'")
