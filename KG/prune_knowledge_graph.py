#!/usr/bin/env python3
"""
Knowledge Graph Pruning Tool

This script takes a knowledge graph and excludes specified entity types and relationship types,
creating a new pruned knowledge graph.
"""

import json
import argparse
from pathlib import Path
import sys
from collections import defaultdict, Counter


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


def save_knowledge_graph(kg, file_path):
    """Save knowledge graph to JSON file."""
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(kg, f, indent=2, ensure_ascii=False)
        print(f"✅ Pruned knowledge graph saved to: {file_path}")
    except Exception as e:
        print(f"Error saving file '{file_path}': {e}")
        sys.exit(1)


def prune_entities(nodes, exclude_types):
    """Remove entities with specified types."""
    if not exclude_types:
        return nodes, set()
    
    exclude_types = set(exclude_types)
    pruned_nodes = []
    removed_node_ids = set()
    
    for node in nodes:
        node_type = node.get('type', 'unknown')
        if node_type in exclude_types:
            removed_node_ids.add(node.get('id'))
        else:
            pruned_nodes.append(node)
    
    return pruned_nodes, removed_node_ids


def prune_relationships(links, exclude_types, removed_node_ids):
    """Remove relationships with specified types and relationships connected to removed nodes."""
    if not exclude_types:
        exclude_types = set()
    else:
        exclude_types = set(exclude_types)
    
    pruned_links = []
    
    for link in links:
        # Check relationship type
        rel_type = link.get('type', link.get('relationship', link.get('label', 'unknown')))
        if rel_type in exclude_types:
            continue
        
        # Check if source or target nodes were removed
        source = link.get('source', link.get('from'))
        target = link.get('target', link.get('to'))
        
        if source in removed_node_ids or target in removed_node_ids:
            continue
        
        pruned_links.append(link)
    
    return pruned_links


def remove_isolated_nodes(nodes, links):
    """Remove nodes that have no connections (isolated nodes)."""
    # Get all node IDs that appear in links
    connected_node_ids = set()
    for link in links:
        source = link.get('source', link.get('from'))
        target = link.get('target', link.get('to'))
        if source:
            connected_node_ids.add(source)
        if target:
            connected_node_ids.add(target)
    
    # Keep only nodes that are connected
    connected_nodes = []
    isolated_nodes = []
    
    for node in nodes:
        node_id = node.get('id')
        if node_id in connected_node_ids:
            connected_nodes.append(node)
        else:
            isolated_nodes.append(node)
    
    return connected_nodes, isolated_nodes


def update_metadata(metadata, original_nodes, original_links, pruned_nodes, pruned_links):
    """Update metadata with new counts and statistics."""
    if not metadata:
        metadata = {}
    
    # Update basic counts
    metadata['total_nodes'] = len(pruned_nodes)
    metadata['total_edges'] = len(pruned_links)
    
    # Update node type counts
    if 'node_types' in metadata:
        node_types = Counter()
        for node in pruned_nodes:
            node_type = node.get('type', 'unknown')
            node_types[node_type] += 1
        metadata['node_types'] = dict(node_types)
    
    # Update relationship type counts
    if 'relationship_types' in metadata:
        rel_types = Counter()
        for link in pruned_links:
            rel_type = link.get('type', link.get('relationship', link.get('label', 'unknown')))
            rel_types[rel_type] += 1
        metadata['relationship_types'] = dict(rel_types)
    
    # Add pruning information
    metadata['pruning_info'] = {
        'original_nodes': len(original_nodes),
        'original_links': len(original_links),
        'pruned_nodes': len(pruned_nodes),
        'pruned_links': len(pruned_links),
        'nodes_removed': len(original_nodes) - len(pruned_nodes),
        'links_removed': len(original_links) - len(pruned_links)
    }
    
    return metadata


def print_pruning_summary(original_kg, pruned_kg, exclude_entity_types, exclude_relationship_types, isolated_nodes_removed=None):
    """Print a summary of the pruning operation."""
    original_nodes = len(original_kg.get('nodes', []))
    original_links = len(original_kg.get('links', []))
    pruned_nodes = len(pruned_kg.get('nodes', []))
    pruned_links = len(pruned_kg.get('links', []))
    
    print(f"\n{'='*60}")
    print(f"PRUNING SUMMARY")
    print(f"{'='*60}")
    
    print(f"\n📊 BEFORE PRUNING:")
    print(f"   Nodes: {original_nodes}")
    print(f"   Links: {original_links}")
    
    print(f"\n📊 AFTER PRUNING:")
    print(f"   Nodes: {pruned_nodes}")
    print(f"   Links: {pruned_links}")
    
    print(f"\n🗑️  REMOVED:")
    print(f"   Nodes: {original_nodes - pruned_nodes}")
    print(f"   Links: {original_links - pruned_links}")
    
    if isolated_nodes_removed:
        print(f"   Isolated nodes: {len(isolated_nodes_removed)}")
    
    if exclude_entity_types:
        print(f"\n🚫 EXCLUDED ENTITY TYPES:")
        for entity_type in exclude_entity_types:
            print(f"   • {entity_type}")
    
    if exclude_relationship_types:
        print(f"\n🚫 EXCLUDED RELATIONSHIP TYPES:")
        for rel_type in exclude_relationship_types:
            print(f"   • {rel_type}")
    
    # Calculate percentages
    if original_nodes > 0:
        nodes_kept_pct = (pruned_nodes / original_nodes) * 100
        print(f"\n📈 RETENTION RATE:")
        print(f"   Nodes: {nodes_kept_pct:.1f}% retained")
    
    if original_links > 0:
        links_kept_pct = (pruned_links / original_links) * 100
        print(f"   Links: {links_kept_pct:.1f}% retained")


def list_available_types(kg):
    """List all available entity and relationship types in the knowledge graph."""
    nodes = kg.get('nodes', [])
    links = kg.get('links', [])
    
    # Count entity types
    entity_types = Counter()
    for node in nodes:
        node_type = node.get('type', 'unknown')
        entity_types[node_type] += 1
    
    # Count relationship types
    rel_types = Counter()
    for link in links:
        rel_type = link.get('type', link.get('relationship', link.get('label', 'unknown')))
        rel_types[rel_type] += 1
    
    print(f"\n📋 AVAILABLE ENTITY TYPES:")
    for entity_type, count in entity_types.most_common():
        print(f"   • {entity_type}: {count}")
    
    print(f"\n📋 AVAILABLE RELATIONSHIP TYPES:")
    for rel_type, count in rel_types.most_common():
        print(f"   • {rel_type}: {count}")


def main():
    parser = argparse.ArgumentParser(description='Prune knowledge graph by excluding specified entity and relationship types')
    parser.add_argument('input_file', help='Input knowledge graph JSON file')
    parser.add_argument('output_file', help='Output pruned knowledge graph JSON file')
    parser.add_argument('--exclude-entities', nargs='+', help='Entity types to exclude', default=[])
    parser.add_argument('--exclude-relationships', nargs='+', help='Relationship types to exclude', default=[])
    parser.add_argument('--remove-isolated', action='store_true', help='Remove nodes with no connections')
    parser.add_argument('--list-types', action='store_true', help='List all available types and exit')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be pruned without saving')
    
    args = parser.parse_args()
    
    # Load knowledge graph
    kg = load_knowledge_graph(args.input_file)
    
    # List types if requested
    if args.list_types:
        list_available_types(kg)
        return
    
    # Validate that we have something to exclude
    if not args.exclude_entities and not args.exclude_relationships:
        print("Error: You must specify at least one entity type or relationship type to exclude.")
        print("Use --list-types to see available types.")
        sys.exit(1)
    
    # Extract components
    original_nodes = kg.get('nodes', [])
    original_links = kg.get('links', [])
    original_metadata = kg.get('metadata', {})
    
    # Prune entities
    pruned_nodes, removed_node_ids = prune_entities(original_nodes, args.exclude_entities)
    
    # Prune relationships
    pruned_links = prune_relationships(original_links, args.exclude_relationships, removed_node_ids)
    
    # Remove isolated nodes if requested
    isolated_nodes_removed = []
    if args.remove_isolated:
        pruned_nodes, isolated_nodes_removed = remove_isolated_nodes(pruned_nodes, pruned_links)
    
    # Create pruned knowledge graph
    pruned_kg = {
        'nodes': pruned_nodes,
        'links': pruned_links
    }
    
    # Update metadata
    if original_metadata:
        pruned_metadata = update_metadata(original_metadata, original_nodes, original_links, 
                                        pruned_nodes, pruned_links)
        pruned_kg['metadata'] = pruned_metadata
    
    # Print summary
    print_pruning_summary(kg, pruned_kg, args.exclude_entities, args.exclude_relationships, isolated_nodes_removed)
    
    # Save or show dry run
    if args.dry_run:
        print(f"\n🔍 DRY RUN: Would save pruned graph to '{args.output_file}'")
        print("   Use without --dry-run to actually save the file.")
    else:
        save_knowledge_graph(pruned_kg, args.output_file)


if __name__ == '__main__':
    main()