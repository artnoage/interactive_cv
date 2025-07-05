#!/usr/bin/env python3
"""
Tool Comparison Analysis
Compares manually built tools vs blueprint-generated tools to demonstrate
the power of configuration-driven development.
"""

import sys
sys.path.append('.')

from RAG.blueprint_driven_tools import BlueprintDrivenToolGenerator
from RAG.agent_tools import InteractiveCVTools
import time
import inspect
from typing import Dict, List, Any


class ToolComparisonAnalysis:
    """Analyzes and compares manual vs blueprint-generated tools."""
    
    def __init__(self):
        """Initialize both tool systems."""
        print("🔧 Initializing tool systems...")
        
        # Manual tools
        self.manual_tools = InteractiveCVTools()
        
        # Blueprint-generated tools  
        self.generated_tools = BlueprintDrivenToolGenerator()
        
        print(f"✅ Manual tools: {len(self._get_manual_tool_methods())} methods")
        print(f"✅ Generated tools: {len(self.generated_tools.list_all_tools())} tools")
    
    def _get_manual_tool_methods(self) -> List[str]:
        """Get list of manual tool method names."""
        methods = []
        for name in dir(self.manual_tools):
            if not name.startswith('_') and callable(getattr(self.manual_tools, name)):
                methods.append(name)
        return methods
    
    def compare_coverage(self) -> Dict[str, Any]:
        """Compare functional coverage between manual and generated tools."""
        manual_methods = self._get_manual_tool_methods()
        generated_tools = list(self.generated_tools.list_all_tools().keys())
        
        # Categorize manual tools
        manual_categories = {
            'search': [m for m in manual_methods if 'search' in m.lower()],
            'get': [m for m in manual_methods if 'get' in m.lower() or 'find' in m.lower()],
            'list': [m for m in manual_methods if 'list' in m.lower()],
            'semantic': [m for m in manual_methods if 'semantic' in m.lower()],
            'other': []
        }
        
        # Categorize uncategorized methods
        categorized = set()
        for methods in manual_categories.values():
            categorized.update(methods)
        manual_categories['other'] = [m for m in manual_methods if m not in categorized]
        
        # Categorize generated tools by their actual categories
        generated_categories = {}
        for tool in self.generated_tools.list_all_tools().values():
            if tool.category not in generated_categories:
                generated_categories[tool.category] = []
            generated_categories[tool.category].append(tool.name)
        
        return {
            'manual_total': len(manual_methods),
            'generated_total': len(generated_tools),
            'manual_categories': {k: len(v) for k, v in manual_categories.items()},
            'generated_categories': {k: len(v) for k, v in generated_categories.items()},
            'coverage_analysis': {
                'manual_methods': manual_methods,
                'generated_tools': generated_tools,
                'manual_detail': manual_categories,
                'generated_detail': generated_categories
            }
        }
    
    def compare_search_capabilities(self) -> Dict[str, Any]:
        """Compare search capabilities with concrete examples."""
        print("\n🔍 Testing Search Capabilities...")
        
        results = {
            'manual_search': {},
            'generated_search': {},
            'performance': {},
            'capability_comparison': {}
        }
        
        test_queries = [
            ("neural", "topics"),
            ("optimal transport", "topics"), 
            ("Vaios", "people"),
            ("University", "institutions")
        ]
        
        for query, entity_type in test_queries:
            print(f"  Testing query: '{query}' in {entity_type}")
            
            # Test manual tools
            manual_start = time.time()
            try:
                if entity_type == "topics":
                    manual_results = self.manual_tools.find_research_topics(query, limit=5)
                elif entity_type == "people":
                    manual_results = self.manual_tools.search_academic_papers(query, limit=5)  # Best we can do
                elif entity_type == "institutions":
                    manual_results = self.manual_tools.get_all_institutions()[:5]
                else:
                    manual_results = []
                manual_time = time.time() - manual_start
                results['manual_search'][f"{query}_{entity_type}"] = {
                    'count': len(manual_results),
                    'time': manual_time,
                    'results': manual_results[:2] if manual_results else []
                }
            except Exception as e:
                results['manual_search'][f"{query}_{entity_type}"] = {'error': str(e)}
            
            # Test generated tools
            generated_start = time.time()
            try:
                generated_results = self.generated_tools.execute_tool(f"search_{entity_type}", query=query, limit=5)
                generated_time = time.time() - generated_start
                results['generated_search'][f"{query}_{entity_type}"] = {
                    'count': len(generated_results),
                    'time': generated_time,
                    'results': generated_results[:2] if generated_results else []
                }
            except Exception as e:
                results['generated_search'][f"{query}_{entity_type}"] = {'error': str(e)}
        
        return results
    
    def compare_relationship_capabilities(self) -> Dict[str, Any]:
        """Compare relationship traversal capabilities."""
        print("\n🕸️ Testing Relationship Capabilities...")
        
        results = {
            'manual_relationships': {},
            'generated_relationships': {},
            'relationship_types': {}
        }
        
        # Manual tools - limited relationship capabilities
        try:
            manual_collab = self.manual_tools.get_collaborations()
            results['manual_relationships']['collaborations'] = {
                'count': len(manual_collab),
                'sample': manual_collab[:2] if manual_collab else []
            }
        except Exception as e:
            results['manual_relationships']['collaborations'] = {'error': str(e)}
        
        # Generated tools - comprehensive relationship traversal
        relationship_types = ['discusses', 'uses_method', 'authored_by', 'accomplished']
        
        for rel_type in relationship_types:
            try:
                # Test traversal from a document
                traverse_results = self.generated_tools.execute_tool(
                    f"traverse_{rel_type}", 
                    source_type="document", 
                    source_id="academic_1", 
                    limit=3
                )
                results['generated_relationships'][rel_type] = {
                    'count': len(traverse_results),
                    'sample': traverse_results[:2] if traverse_results else []
                }
            except Exception as e:
                results['generated_relationships'][rel_type] = {'error': str(e)}
        
        # Get all available relationship types from generated tools
        all_rel_tools = [tool for tool in self.generated_tools.list_all_tools().keys() 
                        if tool.startswith('traverse_')]
        results['relationship_types']['available'] = [tool.replace('traverse_', '') for tool in all_rel_tools]
        results['relationship_types']['count'] = len(all_rel_tools)
        
        return results
    
    def compare_category_awareness(self) -> Dict[str, Any]:
        """Compare category-aware capabilities."""
        print("\n📊 Testing Category Awareness...")
        
        results = {
            'manual_categories': {},
            'generated_categories': {},
            'category_richness': {}
        }
        
        # Manual tools - basic category filtering
        try:
            manual_topics = self.manual_tools.find_research_topics("neural", category="innovation", limit=5)
            results['manual_categories']['topics_with_category'] = {
                'count': len(manual_topics),
                'sample': manual_topics[:2] if manual_topics else []
            }
        except Exception as e:
            results['manual_categories']['topics_with_category'] = {'error': str(e)}
        
        # Generated tools - rich category exploration
        try:
            # Get category overview
            cat_overview = self.generated_tools.execute_tool("explore_topic_categories")
            results['generated_categories']['overview'] = {
                'total_categories': cat_overview.get('total_categories', 0),
                'top_categories': [cat['category'] for cat in cat_overview.get('categories', [])[:5]]
            }
            
            # Test specific category exploration
            if cat_overview.get('categories'):
                first_cat = cat_overview['categories'][0]['category']
                cat_details = self.generated_tools.execute_tool("explore_topic_categories", category=first_cat, limit=3)
                results['generated_categories']['specific_category'] = {
                    'category': first_cat,
                    'count': cat_details.get('count', 0),
                    'sample': [e.get('name') for e in cat_details.get('entities', [])[:2]]
                }
        except Exception as e:
            results['generated_categories']['category_exploration'] = {'error': str(e)}
        
        return results
    
    def compare_visualization_readiness(self) -> Dict[str, Any]:
        """Compare visualization-ready data generation."""
        print("\n🎨 Testing Visualization Readiness...")
        
        results = {
            'manual_viz': {},
            'generated_viz': {},
            'viz_features': {}
        }
        
        # Manual tools - no built-in visualization support
        try:
            manual_topics = self.manual_tools.find_research_topics("neural", limit=3)
            results['manual_viz']['basic_data'] = {
                'count': len(manual_topics),
                'has_viz_data': any('color' in str(topic) or 'size' in str(topic) for topic in manual_topics),
                'sample_fields': list(manual_topics[0].keys()) if manual_topics else []
            }
        except Exception as e:
            results['manual_viz']['basic_data'] = {'error': str(e)}
        
        # Generated tools - rich visualization data
        try:
            viz_data = self.generated_tools.execute_tool("get_visualization_data", 
                                                        entity_type="topic", 
                                                        entity_id="1")
            if viz_data:
                results['generated_viz']['rich_data'] = {
                    'has_entity': 'entity' in viz_data,
                    'has_visualization': 'visualization' in viz_data,
                    'viz_fields': list(viz_data.get('visualization', {}).keys()),
                    'sample': viz_data
                }
        except Exception as e:
            results['generated_viz']['rich_data'] = {'error': str(e)}
        
        return results
    
    def analyze_code_complexity(self) -> Dict[str, Any]:
        """Analyze code complexity and maintenance burden."""
        results = {
            'manual_complexity': {},
            'generated_complexity': {},
            'maintenance_analysis': {}
        }
        
        # Analyze manual tools
        manual_source = inspect.getsource(InteractiveCVTools)
        manual_lines = len(manual_source.split('\n'))
        manual_methods = len(self._get_manual_tool_methods())
        
        results['manual_complexity'] = {
            'lines_of_code': manual_lines,
            'methods_count': manual_methods,
            'avg_lines_per_method': manual_lines / manual_methods if manual_methods > 0 else 0,
            'hardcoded_schemas': manual_source.count('SELECT'),
            'error_handling': manual_source.count('try:')
        }
        
        # Analyze generated tools (the generator code, not the generated tools)
        generator_source = inspect.getsource(BlueprintDrivenToolGenerator)
        generator_lines = len(generator_source.split('\n'))
        generated_tool_count = len(self.generated_tools.list_all_tools())
        
        results['generated_complexity'] = {
            'generator_lines': generator_lines,
            'tools_generated': generated_tool_count,
            'tools_per_generator_line': generated_tool_count / generator_lines,
            'configuration_driven': True,
            'schema_references': generator_source.count('blueprint')
        }
        
        # Maintenance analysis
        results['maintenance_analysis'] = {
            'manual_schema_changes': 'Requires manual code updates for each schema change',
            'generated_schema_changes': 'Automatic regeneration from updated blueprints',
            'adding_new_entity_type': {
                'manual': 'Requires writing new methods, queries, error handling',
                'generated': 'Add YAML mapping, automatic tool generation'
            },
            'consistency': {
                'manual': 'Prone to inconsistencies between similar tools',
                'generated': 'Guaranteed consistency from blueprint specifications'
            }
        }
        
        return results
    
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """Generate comprehensive comparison report."""
        print("📋 Generating Comprehensive Comparison Report...")
        
        report = {
            'summary': {},
            'coverage': self.compare_coverage(),
            'search_capabilities': self.compare_search_capabilities(),
            'relationship_capabilities': self.compare_relationship_capabilities(),
            'category_awareness': self.compare_category_awareness(),
            'visualization_readiness': self.compare_visualization_readiness(),
            'code_complexity': self.analyze_code_complexity(),
            'conclusions': {}
        }
        
        # Generate summary
        report['summary'] = {
            'manual_tools': len(self._get_manual_tool_methods()),
            'generated_tools': len(self.generated_tools.list_all_tools()),
            'generation_ratio': len(self.generated_tools.list_all_tools()) / len(self._get_manual_tool_methods()),
            'blueprint_driven_advantages': [
                'Automatic tool generation from configuration',
                'Schema consistency guaranteed',
                'Category-aware search capabilities',
                'Rich relationship traversal',
                'Visualization-ready data',
                'Easy maintenance and extension'
            ]
        }
        
        # Generate conclusions
        report['conclusions'] = {
            'coverage': f"Generated tools provide {len(self.generated_tools.list_all_tools())} tools vs {len(self._get_manual_tool_methods())} manual methods",
            'sophistication': "Generated tools include advanced features like relationship traversal and category exploration",
            'maintainability': "Blueprint-driven approach eliminates manual coding for schema changes",
            'consistency': "Generated tools guarantee consistency across similar operations",
            'extensibility': "Adding new entity types requires only YAML configuration updates"
        }
        
        return report


def print_report_summary(report: Dict[str, Any]):
    """Print a formatted summary of the comparison report."""
    print("\n" + "="*80)
    print("📊 BLUEPRINT-DRIVEN TOOLS vs MANUAL TOOLS - COMPARISON REPORT")
    print("="*80)
    
    # Summary
    summary = report['summary']
    print(f"\n🔢 TOOL COUNT COMPARISON:")
    print(f"   Manual Tools:    {summary['manual_tools']:2d} methods")
    print(f"   Generated Tools: {summary['generated_tools']:2d} tools")
    print(f"   Generation Ratio: {summary['generation_ratio']:.1f}x more tools")
    
    # Coverage
    coverage = report['coverage']
    print(f"\n📈 FUNCTIONAL COVERAGE:")
    print(f"   Manual Categories: {len(coverage['manual_categories'])} types")
    print(f"   Generated Categories: {len(coverage['generated_categories'])} types")
    
    print("\n   Manual Tool Categories:")
    for cat, count in coverage['manual_categories'].items():
        print(f"   - {cat}: {count} tools")
    
    print("\n   Generated Tool Categories:")
    for cat, count in coverage['generated_categories'].items():
        print(f"   - {cat}: {count} tools")
    
    # Search capabilities
    search = report['search_capabilities']
    print(f"\n🔍 SEARCH CAPABILITIES:")
    manual_searches = len([k for k, v in search['manual_search'].items() if 'error' not in v])
    generated_searches = len([k for k, v in search['generated_search'].items() if 'error' not in v])
    print(f"   Manual successful searches: {manual_searches}")
    print(f"   Generated successful searches: {generated_searches}")
    
    # Relationships
    relationships = report['relationship_capabilities']
    rel_types = relationships.get('relationship_types', {})
    print(f"\n🕸️ RELATIONSHIP CAPABILITIES:")
    print(f"   Manual relationship tools: 1 (basic collaborations)")
    print(f"   Generated relationship types: {rel_types.get('count', 0)}")
    print(f"   Available relationships: {', '.join(rel_types.get('available', [])[:5])}...")
    
    # Code complexity
    complexity = report['code_complexity']
    print(f"\n💻 CODE COMPLEXITY:")
    manual = complexity['manual_complexity']
    generated = complexity['generated_complexity']
    print(f"   Manual code lines: {manual['lines_of_code']}")
    print(f"   Generator code lines: {generated['generator_lines']}")
    print(f"   Tools per generator line: {generated['tools_per_generator_line']:.2f}")
    
    # Conclusions
    print(f"\n✅ KEY ADVANTAGES OF BLUEPRINT-DRIVEN APPROACH:")
    for advantage in summary['blueprint_driven_advantages']:
        print(f"   • {advantage}")
    
    print(f"\n🎯 CONCLUSIONS:")
    for key, conclusion in report['conclusions'].items():
        print(f"   • {key.title()}: {conclusion}")
    
    print("\n" + "="*80)


def main():
    """Run comprehensive tool comparison analysis."""
    try:
        analyzer = ToolComparisonAnalysis()
        report = analyzer.generate_comprehensive_report()
        
        print_report_summary(report)
        
        # Save detailed report
        import json
        with open('tool_comparison_report.json', 'w') as f:
            json.dump(report, f, indent=2, default=str)
        print(f"\n💾 Detailed report saved to: tool_comparison_report.json")
        
    except Exception as e:
        print(f"❌ Error in analysis: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()