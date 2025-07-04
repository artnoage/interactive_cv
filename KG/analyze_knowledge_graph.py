#!/usr/bin/env python3
"""
Knowledge Graph Analysis Tool

This script analyzes knowledge graphs and extracts detailed information about
entities and relationships for comparison purposes.
"""

import json
import argparse
from collections import defaultdict, Counter
from pathlib import Path
import sys


def load_knowledge_graph(file_path):
    """Load knowledge graph from JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in '{file_path}': {e}")
        sys.exit(1)


def analyze_entities(nodes):
    """Analyze entities in the knowledge graph."""
    entities = {
        'total_count': len(nodes),
        'by_type': defaultdict(list),
        'types_count': Counter(),
        'unique_types': set()
    }
    
    for node in nodes:
        node_type = node.get('type', 'unknown')
        entities['by_type'][node_type].append(node)
        entities['types_count'][node_type] += 1
        entities['unique_types'].add(node_type)
    
    return entities


def analyze_relationships(links):
    """Analyze relationships in the knowledge graph."""
    relationships = {
        'total_count': len(links),
        'by_type': defaultdict(list),
        'types_count': Counter(),
        'unique_types': set(),
        'source_target_pairs': []
    }
    
    for link in links:
        # Handle different possible field names for relationship type
        rel_type = link.get('type', link.get('relationship', link.get('label', 'unknown')))
        relationships['by_type'][rel_type].append(link)
        relationships['types_count'][rel_type] += 1
        relationships['unique_types'].add(rel_type)
        
        # Store source-target pairs for connection analysis
        source = link.get('source', link.get('from'))
        target = link.get('target', link.get('to'))
        if source and target:
            relationships['source_target_pairs'].append((source, target, rel_type))
    
    return relationships


def find_common_entities(entities1, entities2):
    """Find entities that appear in both knowledge graphs."""
    # Extract entity identifiers (using id or title/label)
    ids1 = set()
    ids2 = set()
    
    for node in entities1['by_type'].values():
        for entity in node:
            ids1.add(entity.get('id', entity.get('title', entity.get('label', str(entity)))))
    
    for node in entities2['by_type'].values():
        for entity in node:
            ids2.add(entity.get('id', entity.get('title', entity.get('label', str(entity)))))
    
    common = ids1.intersection(ids2)
    only_in_1 = ids1 - ids2
    only_in_2 = ids2 - ids1
    
    return {
        'common': common,
        'only_in_first': only_in_1,
        'only_in_second': only_in_2
    }


def find_common_relationships(relationships1, relationships2):
    """Find relationships that appear in both knowledge graphs."""
    types1 = relationships1['unique_types']
    types2 = relationships2['unique_types']
    
    common_types = types1.intersection(types2)
    only_in_1 = types1 - types2
    only_in_2 = types2 - types1
    
    return {
        'common_types': common_types,
        'only_in_first': only_in_1,
        'only_in_second': only_in_2
    }


def print_analysis_report(file_path, entities, relationships):
    """Print detailed analysis report for a knowledge graph."""
    print(f"\n{'='*60}")
    print(f"ANALYSIS: {file_path}")
    print(f"{'='*60}")
    
    print(f"\n📊 ENTITIES SUMMARY:")
    print(f"   Total Entities: {entities['total_count']}")
    print(f"   Unique Types: {len(entities['unique_types'])}")
    
    print(f"\n📋 ENTITY TYPES:")
    for entity_type, count in entities['types_count'].most_common():
        print(f"   • {entity_type}: {count}")
    
    print(f"\n🔗 RELATIONSHIPS SUMMARY:")
    print(f"   Total Relationships: {relationships['total_count']}")
    print(f"   Unique Types: {len(relationships['unique_types'])}")
    
    print(f"\n📋 RELATIONSHIP TYPES:")
    for rel_type, count in relationships['types_count'].most_common():
        print(f"   • {rel_type}: {count}")


def print_comparison_report(entities1, entities2, relationships1, relationships2, 
                          common_entities, common_relationships, file1_name, file2_name):
    """Print comparison report between two knowledge graphs."""
    print(f"\n{'='*60}")
    print(f"COMPARISON: {file1_name} vs {file2_name}")
    print(f"{'='*60}")
    
    print(f"\n🔍 ENTITIES COMPARISON:")
    print(f"   {file1_name}: {entities1['total_count']} entities")
    print(f"   {file2_name}: {entities2['total_count']} entities")
    print(f"   Common entities: {len(common_entities['common'])}")
    print(f"   Only in {file1_name}: {len(common_entities['only_in_first'])}")
    print(f"   Only in {file2_name}: {len(common_entities['only_in_second'])}")
    
    print(f"\n📊 ENTITY TYPES COMPARISON:")
    all_types = entities1['unique_types'].union(entities2['unique_types'])
    for entity_type in sorted(all_types):
        count1 = entities1['types_count'].get(entity_type, 0)
        count2 = entities2['types_count'].get(entity_type, 0)
        print(f"   • {entity_type}: {count1} vs {count2}")
    
    print(f"\n🔗 RELATIONSHIPS COMPARISON:")
    print(f"   {file1_name}: {relationships1['total_count']} relationships")
    print(f"   {file2_name}: {relationships2['total_count']} relationships")
    print(f"   Common types: {len(common_relationships['common_types'])}")
    print(f"   Only in {file1_name}: {len(common_relationships['only_in_first'])}")
    print(f"   Only in {file2_name}: {len(common_relationships['only_in_second'])}")
    
    print(f"\n📋 RELATIONSHIP TYPES COMPARISON:")
    all_rel_types = relationships1['unique_types'].union(relationships2['unique_types'])
    for rel_type in sorted(all_rel_types):
        count1 = relationships1['types_count'].get(rel_type, 0)
        count2 = relationships2['types_count'].get(rel_type, 0)
        print(f"   • {rel_type}: {count1} vs {count2}")
    
    if common_relationships['common_types']:
        print(f"\n✅ COMMON RELATIONSHIP TYPES:")
        for rel_type in sorted(common_relationships['common_types']):
            print(f"   • {rel_type}")
    
    if common_relationships['only_in_first']:
        print(f"\n🔵 ONLY IN {file1_name.upper()}:")
        for rel_type in sorted(common_relationships['only_in_first']):
            print(f"   • {rel_type}")
    
    if common_relationships['only_in_second']:
        print(f"\n🔴 ONLY IN {file2_name.upper()}:")
        for rel_type in sorted(common_relationships['only_in_second']):
            print(f"   • {rel_type}")


def main():
    parser = argparse.ArgumentParser(description='Analyze knowledge graphs and extract entities and relationships')
    parser.add_argument('files', nargs='+', help='Knowledge graph JSON files to analyze')
    parser.add_argument('--compare', action='store_true', help='Compare two knowledge graphs')
    parser.add_argument('--output', help='Output results to file instead of stdout')
    
    args = parser.parse_args()
    
    if len(args.files) < 1:
        print("Error: At least one file is required.")
        sys.exit(1)
    
    if args.compare and len(args.files) != 2:
        print("Error: Exactly two files are required for comparison.")
        sys.exit(1)
    
    # Redirect output if specified
    if args.output:
        sys.stdout = open(args.output, 'w', encoding='utf-8')
    
    try:
        # Load knowledge graphs
        graphs = []
        for file_path in args.files:
            kg = load_knowledge_graph(file_path)
            graphs.append((file_path, kg))
        
        # Analyze each graph
        analyses = []
        for file_path, kg in graphs:
            nodes = kg.get('nodes', [])
            links = kg.get('links', [])
            
            entities = analyze_entities(nodes)
            relationships = analyze_relationships(links)
            
            analyses.append((file_path, entities, relationships))
            
            # Print individual analysis
            print_analysis_report(file_path, entities, relationships)
        
        # Compare if requested
        if args.compare and len(analyses) == 2:
            file1, entities1, relationships1 = analyses[0]
            file2, entities2, relationships2 = analyses[1]
            
            common_entities = find_common_entities(entities1, entities2)
            common_relationships = find_common_relationships(relationships1, relationships2)
            
            print_comparison_report(entities1, entities2, relationships1, relationships2,
                                  common_entities, common_relationships, 
                                  Path(file1).name, Path(file2).name)
    
    finally:
        if args.output:
            sys.stdout.close()
            sys.stdout = sys.__stdout__
            print(f"Results saved to: {args.output}")


if __name__ == '__main__':
    main()