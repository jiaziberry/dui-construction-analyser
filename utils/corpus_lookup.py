#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Corpus-Based Predicate Lookup
=============================
Lookup system based on 394,355 classified 对-constructions from the BCC corpus.
Provides corpus statistics, distribution across types, and contextual analysis.

For Chinese language learners to understand how predicates are typically used
and why certain contexts lead to different classifications.
"""

import json
import os
from typing import Dict, Any, Optional, List, Tuple

# Full names for construction types
TYPE_NAMES = {
    'DA': ('Directed-Action', '指向动作'),
    'SI': ('Scoped-Intervention', '范围干预'),
    'MS': ('Mental-State', '心理状态'),
    'ABT': ('Aboutness', '论题关涉'),
    'EVAL': ('Evaluation', '评价效果'),
    'DISP': ('Disposition', '态度行为'),
}

# Explanations for WHY predicates are classified each way
TYPE_EXPLANATIONS = {
    'DA': {
        'description': 'The speaker/actor directs an action TO a person or recipient.',
        'y_role': 'Y is the recipient who receives the action.',
        'test': 'Ask: Is X doing something TO/AT Y?',
        'examples': ['对他说 (speak TO him)', '对观众鞠躬 (bow TO the audience)'],
    },
    'SI': {
        'description': 'X performs a bounded intervention ON Y. Y is affected or changed.',
        'y_role': 'Y is the scope or patient that undergoes change.',
        'test': 'Ask: Is X intervening ON Y? Is Y affected?',
        'examples': ['对企业进行检查 (conduct inspection ON enterprises)', '对他进行治疗 (provide treatment TO him)'],
    },
    'MS': {
        'description': 'Y triggers an internal psychological state IN X.',
        'y_role': 'Y is the stimulus that causes X\'s mental/emotional state.',
        'test': 'Ask: Does Y trigger a feeling/thought IN X?',
        'examples': ['对此担心 (worried ABOUT this)', '对她有好感 (have good feelings TOWARD her)'],
    },
    'ABT': {
        'description': 'X produces discourse (speech, writing, analysis) ABOUT Y.',
        'y_role': 'Y is the topic of X\'s discourse. Y is not affected.',
        'test': 'Ask: Does X produce observable output ABOUT Y?',
        'examples': ['对此发表意见 (express opinions ABOUT this)', '对问题进行分析 (analyse the problem)'],
    },
    'EVAL': {
        'description': 'X is evaluated as good/bad/useful/harmful FOR Y.',
        'y_role': 'Y is the beneficiary or perspective from which X is judged.',
        'test': 'Ask: Is X good/bad/useful FOR Y?',
        'examples': ['对健康有益 (beneficial FOR health)', '对学生重要 (important FOR students)'],
    },
    'DISP': {
        'description': 'X exhibits a behavioural manner or social attitude TOWARD Y.',
        'y_role': 'Y experiences X\'s manner of treatment.',
        'test': 'Ask: How is X treating/behaving toward Y?',
        'examples': ['对他热情 (warm TOWARD him)', '对客人客气 (polite TOWARD guests)'],
    },
}

# Context markers that can override corpus-based classification
CONTEXT_OVERRIDES = {
    '发表': {
        'ABT_markers': ['意见', '看法', '观点', '声明', '讲话', '评论'],
        'DA_markers': ['微笑', '笑容', '善意'],
        'explanation': '发表 is ABT when producing discourse (意见/看法), but DA when directing expressions TO someone.',
    },
    '表示': {
        'ABT_markers': ['关切', '遗憾', '不满', '欢迎', '支持', '反对'],
        'DA_markers': [],  # Usually becomes ABT with inanimate Y
        'explanation': '表示 is typically ABT when expressing stance ABOUT something.',
    },
    '有': {
        'MS_markers': ['兴趣', '信心', '把握', '好感', '印象', '了解', '感情'],
        'EVAL_markers': ['益', '害', '利', '用', '效', '帮助', '作用', '影响'],
        'ABT_markers': ['意见', '看法', '研究'],
        'explanation': '有 varies by complement: 有+psychological→MS, 有+effect→EVAL, 有+opinion→ABT.',
    },
}


class CorpusLookup:
    """Lookup system for predicate analysis based on BCC corpus data."""
    
    def __init__(self, corpus_file: str = None):
        """
        Initialize the corpus lookup.
        
        Args:
            corpus_file: Path to predicate_corpus.json. If None, uses default location.
        """
        if corpus_file is None:
            # Try to find the corpus file
            possible_paths = [
                os.path.join(os.path.dirname(__file__), '..', 'data', 'predicate_corpus.json'),
                os.path.join(os.path.dirname(__file__), 'data', 'predicate_corpus.json'),
                'data/predicate_corpus.json',
            ]
            for path in possible_paths:
                if os.path.exists(path):
                    corpus_file = path
                    break
        
        self.corpus_data = {}
        if corpus_file and os.path.exists(corpus_file):
            with open(corpus_file, 'r', encoding='utf-8') as f:
                self.corpus_data = json.load(f)
    
    def lookup(self, predicate: str) -> Optional[Dict[str, Any]]:
        """
        Look up a predicate in the corpus data.
        
        Args:
            predicate: The predicate to look up
            
        Returns:
            Dictionary with corpus statistics, or None if not found
        """
        if predicate in self.corpus_data:
            data = self.corpus_data[predicate].copy()
            
            # Add full type names
            dominant = data.get('dominant_type', '')
            if dominant in TYPE_NAMES:
                data['dominant_name'], data['dominant_chinese'] = TYPE_NAMES[dominant]
            
            # Add explanation
            if dominant in TYPE_EXPLANATIONS:
                data['explanation'] = TYPE_EXPLANATIONS[dominant]
            
            return data
        return None
    
    def get_distribution_text(self, predicate: str) -> str:
        """
        Get a human-readable distribution text for a predicate.
        
        Args:
            predicate: The predicate to describe
            
        Returns:
            Formatted string describing the corpus distribution
        """
        data = self.lookup(predicate)
        if not data:
            return f"'{predicate}' was not found in the corpus."
        
        lines = [f"**{predicate}** in the BCC corpus ({data['total']:,} instances):"]
        
        # Sort distribution by percentage
        dist = data.get('distribution', {})
        sorted_dist = sorted(dist.items(), key=lambda x: x[1], reverse=True)
        
        for type_code, pct in sorted_dist:
            if pct > 0:
                full_name, chinese = TYPE_NAMES.get(type_code, (type_code, ''))
                count = data.get('types', {}).get(type_code, 0)
                lines.append(f"- **{full_name}** ({chinese}): {pct:.1f}% ({count:,} instances)")
        
        return '\n'.join(lines)
    
    def analyse_in_context(self, predicate: str, complement: str = '', 
                           y_phrase: str = '', full_sentence: str = '') -> Dict[str, Any]:
        """
        Analyse a predicate in its specific context.
        
        Args:
            predicate: The main predicate
            complement: Text following the predicate
            y_phrase: The Y phrase (object of 对)
            full_sentence: The complete sentence
            
        Returns:
            Analysis with corpus data and contextual interpretation
        """
        corpus_data = self.lookup(predicate) or {}
        context_text = complement + y_phrase + full_sentence
        
        result = {
            'predicate': predicate,
            'corpus_found': bool(corpus_data),
            'corpus_data': corpus_data,
            'contextual_type': None,
            'contextual_reason': None,
            'learning_notes': [],
        }
        
        # Check for context overrides
        if predicate in CONTEXT_OVERRIDES:
            override = CONTEXT_OVERRIDES[predicate]
            
            # Check ABT markers
            for marker in override.get('ABT_markers', []):
                if marker in context_text:
                    result['contextual_type'] = 'ABT'
                    result['contextual_reason'] = f"Contains '{marker}' which indicates discourse/commentary"
                    result['learning_notes'].append(override.get('explanation', ''))
                    break
            
            # Check MS markers
            if not result['contextual_type']:
                for marker in override.get('MS_markers', []):
                    if marker in context_text:
                        result['contextual_type'] = 'MS'
                        result['contextual_reason'] = f"Contains '{marker}' which indicates psychological state"
                        result['learning_notes'].append(override.get('explanation', ''))
                        break
            
            # Check EVAL markers
            if not result['contextual_type']:
                for marker in override.get('EVAL_markers', []):
                    if marker in context_text:
                        result['contextual_type'] = 'EVAL'
                        result['contextual_reason'] = f"Contains '{marker}' which indicates evaluation/effect"
                        result['learning_notes'].append(override.get('explanation', ''))
                        break
        
        # If no override, use corpus dominant type
        if not result['contextual_type'] and corpus_data:
            result['contextual_type'] = corpus_data.get('dominant_type')
            conf = corpus_data.get('confidence', 0)
            result['contextual_reason'] = f"Based on corpus: {conf*100:.0f}% of '{predicate}' instances are this type"
        
        # Add learning notes based on type
        if result['contextual_type'] in TYPE_EXPLANATIONS:
            exp = TYPE_EXPLANATIONS[result['contextual_type']]
            result['learning_notes'].append(exp['test'])
        
        return result
    
    def get_similar_predicates(self, predicate: str, limit: int = 5) -> List[Tuple[str, str, int]]:
        """
        Find predicates with similar classification patterns.
        
        Args:
            predicate: The reference predicate
            limit: Maximum number of similar predicates to return
            
        Returns:
            List of (predicate, dominant_type, count) tuples
        """
        data = self.lookup(predicate)
        if not data:
            return []
        
        target_type = data.get('dominant_type')
        target_conf = data.get('confidence', 0)
        
        similar = []
        for pred, pred_data in self.corpus_data.items():
            if pred == predicate:
                continue
            if pred_data.get('dominant_type') == target_type:
                conf = pred_data.get('confidence', 0)
                # Similar confidence level
                if abs(conf - target_conf) < 0.2:
                    similar.append((pred, target_type, pred_data.get('total', 0)))
        
        # Sort by count and limit
        similar.sort(key=lambda x: x[2], reverse=True)
        return similar[:limit]


def get_type_explanation(type_code: str) -> Dict[str, Any]:
    """Get explanation for a construction type."""
    return TYPE_EXPLANATIONS.get(type_code, {})


def get_type_name(type_code: str) -> Tuple[str, str]:
    """Get full name and Chinese name for a type code."""
    return TYPE_NAMES.get(type_code, (type_code, ''))


# Convenience function
def lookup_predicate(predicate: str) -> Optional[Dict[str, Any]]:
    """Quick lookup of a predicate."""
    lookup = CorpusLookup()
    return lookup.lookup(predicate)


if __name__ == "__main__":
    # Test the lookup
    lookup = CorpusLookup()
    
    test_predicates = ['说', '发表', '有', '热情', '进行']
    
    for pred in test_predicates:
        print(f"\n{'='*60}")
        print(lookup.get_distribution_text(pred))
        
        # Test contextual analysis
        if pred == '发表':
            analysis = lookup.analyse_in_context(pred, complement='意见', y_phrase='此')
            print(f"\nContextual analysis for '对此发表意见':")
            print(f"  Type: {analysis['contextual_type']}")
            print(f"  Reason: {analysis['contextual_reason']}")
