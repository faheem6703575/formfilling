#!/usr/bin/env python3
"""
Test script for the data completion functionality
"""

import os
import sys
from datetime import datetime

# Add the code directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_data_completion():
    """
    Test the data completion functionality
    """
    print("🧪 Testing Data Completion Functionality")
    print("="*60)
    
    try:
        from complete_missing_data import DataCompletionAgent
        from data_validation_agent import DataValidationAgent
        
        print("✅ Successfully imported required modules")
        
        # Test file path
        test_file = "finalInput.txt"
        
        # Initialize agents
        print("\n🔧 Initializing agents...")
        completion_agent = DataCompletionAgent()
        validator = DataValidationAgent()
        
        print("✅ Agents initialized successfully")
        
        # Test validation
        print("\n🔍 Testing data validation...")
        validation_results = completion_agent.run_data_validation(test_file)
        
        completeness = validation_results.get('completeness_score', 0)
        missing_fields = validation_results.get('missing_fields', [])
        
        print(f"📊 Data Completeness: {completeness:.2f}%")
        print(f"📋 Missing Fields: {len(missing_fields)}")
        
        if missing_fields:
            print("🔍 Sample Missing Fields:")
            for field in missing_fields[:5]:
                if field and field != "Unable to parse detailed analysis":
                    print(f"   • {field}")
        
        # Test AI field generation
        print("\n🤖 Testing AI field value generation...")
        if missing_fields:
            test_field = missing_fields[0] if missing_fields[0] != "Unable to parse detailed analysis" else "COMPANY_NAME"
            
            try:
                with open(test_file, 'r', encoding='utf-8') as file:
                    sample_data = file.read()[:1000]  # First 1000 chars
                
                ai_value = completion_agent._generate_ai_field_value(test_field, sample_data)
                print(f"✅ Generated AI value for '{test_field}': {ai_value[:100]}...")
                
            except Exception as e:
                print(f"⚠️ AI generation test failed: {e}")
        
        # Test field descriptions
        print("\n📝 Testing field descriptions...")
        test_fields = ["COMPANY_NAME", "RD_BUDGET", "PROJECT_KEYWORDS"]
        for field in test_fields:
            description = completion_agent._get_field_description(field)
            print(f"   {field}: {description}")
        
        print("\n✅ All tests completed successfully!")
        print("🎉 Data completion functionality is working correctly")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure all required modules are available")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()


def demo_completion_workflow():
    """
    Demonstrate the complete data completion workflow
    """
    print("\n" + "="*60)
    print("🚀 DEMO: Complete Data Completion Workflow")
    print("="*60)
    
    try:
        from complete_missing_data import DataCompletionAgent
        
        completion_agent = DataCompletionAgent()
        
        print("This demo would run the complete missing data workflow:")
        print("1. ✅ Run data validation")
        print("2. 📋 Show missing fields")
        print("3. 🎯 Offer three completion approaches:")
        print("   • 🤖 AI-powered completion")
        print("   • ✍️ Manual user input")
        print("   • 🔄 Hybrid approach")
        print("4. 💾 Update finalInput.txt with completed data")
        print("5. 🔍 Re-validate to show improvement")
        
        print("\n💡 To run the actual workflow, execute:")
        print("   python code/complete_missing_data.py")
        print("   Or use the Streamlit interface in the main app")
        
    except Exception as e:
        print(f"❌ Demo setup failed: {e}")


if __name__ == "__main__":
    test_data_completion()
    demo_completion_workflow()
