#!/usr/bin/env python3
"""
Test script for the PDF download feature
Run this script to verify that PDF generation works correctly
"""

import os
import sys
import tempfile
import shutil
from datetime import datetime

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_pdf_generation():
    """Test the PDF generation functionality"""
    print("🧪 Testing PDF Generation Feature...")
    
    try:
        # Import the PDF generator
        from pdf_generator import BusinessPlanPDFGenerator
        print("✅ Successfully imported PDF generator")
        
        # Create sample session state data
        sample_session = {
            'trl_result': {
                'trl_level': '4',
                'upgrade_result': {
                    'upgraded_idea': 'This is a sample innovative technology solution for renewable energy optimization. It demonstrates advanced AI-powered systems for energy management and sustainability.',
                    'technical_risks': 'Sample technical risks include system integration challenges and scalability issues.',
                    'mitigation_strategies': 'Risk mitigation strategies include phased deployment and comprehensive testing protocols.'
                }
            },
            'frascati_result': {
                'basic_research_score': '85%',
                'applied_research_score': '90%',
                'experimental_development_score': '88%',
                'overall_classification': 'Applied Research',
                'confidence_level': 'High'
            },
            'market_result': {
                'patent_summary': 'Sample patent search results show moderate competition in the renewable energy sector.',
                'market_saturation': 'Market analysis indicates growing demand with room for innovation.',
                'competitive_analysis': 'Competitive landscape shows established players with opportunities for disruption.'
            },
            'sme_result': {
                'company_size': 'Small Enterprise',
                'employee_count': '25',
                'annual_turnover': '€2.5M',
                'balance_sheet_total': '€1.8M',
                'eligibility_status': 'Eligible',
                'confidence_level': 'High'
            },
            'comprehensive_data': {
                'final_data': {
                    'project_title': 'AI-Powered Renewable Energy Management System',
                    'project_description': 'Advanced AI system for optimizing renewable energy production and distribution',
                    'project_duration': '24 months',
                    'total_budget': '€500,000',
                    'team_size': '8 researchers',
                    'technology_area': 'Artificial Intelligence & Renewable Energy'
                }
            },
            'document_results': {
                'declaration_result': {'success': True},
                'mtep_result': {'success': True},
                'rd_assessment_result': {'success': True},
                'passthrough_result': {'success': True}
            },
            'excel_processing_result': {
                'success': True,
                'output_files': [
                    {'description': '1A Attachment - Project Details & Staff', 'filename': 'ENGLISH_1A priedas_InoStartas en.xlsx', 'status': 'Completed'},
                    {'description': '1B Attachment - Patenting & Commercialization', 'filename': 'ENGISH_1B priedas_InoStartas en.xlsx', 'status': 'Completed'},
                    {'description': 'Financial Plan', 'filename': 'ENGLISH_Finansinis planas en.xlsx', 'status': 'Completed'},
                    {'description': 'Work Remuneration Form', 'filename': 'engish_rekomenduojama_forma_de_____l_planuojamo_darbo_uz_____mokesc_____io_en.xlsx', 'status': 'Completed'}
                ]
            }
        }
        
        print("✅ Created sample session data")
        
        # Initialize PDF generator
        generator = BusinessPlanPDFGenerator()
        print("✅ Initialized PDF generator")
        
        # Test PDF generation
        print("📄 Generating PDF...")
        pdf_buffer = generator.generate_business_plan_pdf(sample_session)
        
        if pdf_buffer:
            print("✅ PDF generated successfully!")
            
            # Save PDF to temporary file for verification
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                tmp_file.write(pdf_buffer.getvalue())
                tmp_filename = tmp_file.name
            
            # Check file size
            file_size = os.path.getsize(tmp_filename)
            print(f"📊 PDF file size: {file_size / 1024:.2f} KB")
            
            # Clean up temporary file
            os.unlink(tmp_filename)
            
            # Test ZIP creation
            print("📦 Testing ZIP creation...")
            zip_buffer = generator.create_zip_with_all_files(sample_session)
            
            if zip_buffer:
                print("✅ ZIP package created successfully!")
                zip_size = len(zip_buffer.getvalue())
                print(f"📊 ZIP file size: {zip_size / 1024:.2f} KB")
            else:
                print("❌ ZIP creation failed")
                
        else:
            print("❌ PDF generation failed")
            return False
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False
    
    return True

def test_data_downloader():
    """Test the data downloader functionality"""
    print("\n🧪 Testing Data Downloader Feature...")
    
    try:
        # Import the data downloader
        from data_downloader import DataDownloader
        print("✅ Successfully imported data downloader")
        
        # Initialize downloader
        downloader = DataDownloader()
        print("✅ Initialized data downloader")
        
        # Test getting Excel files info
        excel_files = downloader.get_excel_files_info()
        print(f"📊 Found {len(excel_files)} Excel files")
        
        # Test getting document files info
        doc_files = downloader.get_document_files_info()
        print(f"📄 Found {len(doc_files)} document files")
        
        # Test Excel ZIP creation if files exist
        if excel_files:
            print("📈 Testing Excel ZIP creation...")
            excel_zip = downloader.download_all_excel_files()
            if excel_zip:
                print("✅ Excel ZIP created successfully!")
            else:
                print("❌ Excel ZIP creation failed")
        else:
            print("ℹ️ No Excel files to test")
        
        # Test document ZIP creation if files exist
        if doc_files:
            print("📄 Testing document ZIP creation...")
            doc_zip = downloader.download_all_document_files()
            if doc_zip:
                print("✅ Document ZIP created successfully!")
            else:
                print("❌ Document ZIP creation failed")
        else:
            print("ℹ️ No document files to test")
            
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False
    
    return True

def main():
    """Main test function"""
    print("🚀 Starting PDF Download Feature Tests")
    print("=" * 50)
    
    # Test PDF generation
    pdf_test_passed = test_pdf_generation()
    
    # Test data downloader
    downloader_test_passed = test_data_downloader()
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    if pdf_test_passed:
        print("✅ PDF Generation: PASSED")
    else:
        print("❌ PDF Generation: FAILED")
    
    if downloader_test_passed:
        print("✅ Data Downloader: PASSED")
    else:
        print("❌ Data Downloader: FAILED")
    
    if pdf_test_passed and downloader_test_passed:
        print("\n🎉 ALL TESTS PASSED! The PDF download feature is working correctly.")
        print("\n📚 Next steps:")
        print("1. Run the main application: streamlit run app.py")
        print("2. Complete at least the TRL analysis step")
        print("3. Use the download buttons to generate PDFs and ZIP packages")
    else:
        print("\n⚠️ Some tests failed. Please check the error messages above.")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check that all required files exist in the correct locations")
        print("3. Verify Python version compatibility (Python 3.7+)")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    main()
