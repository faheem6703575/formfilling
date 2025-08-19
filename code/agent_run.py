import time

from code.agents.ENGISH_1B_priedas_InoStartas_en.Patenting.patenting import main_patenting
from code.agents.ENGISH_1B_priedas_InoStartas_en.Commercialization.commercialisat import main_commercilisat
from code.merge_sheets import merge_excels_to_subsheets_one

from code.agents.ENGLISH_Finansinis_planas_en.revenue_forecast import main_forecast

from code.agents.ENGISH_Rekomenduojamaforma_en.Certificate_for_Budgetary_Authorization.Certificate_for_budgetary_autho import main_budgetary_auth
from code.agents.ENGISH_Rekomenduojamaforma_en.Other_Non_Budgetary.budgetary import main_nonbudgetary
from code.merge_sheets import merge_excels_to_subsheets_two

from code.agents.ENGLISH_1A_priedas_InoStartas_en.Summary.Summary import mainsummary
from code.agents.ENGLISH_1A_priedas_InoStartas_en.Staff.Staff import mainstaff
from code.agents.ENGLISH_1A_priedas_InoStartas_en.Data.data import maindata
from code.agents.ENGLISH_1A_priedas_InoStartas_en.tab1.tab1 import main1
from code.agents.ENGLISH_1A_priedas_InoStartas_en.tab2.tab2 import main2
from code.agents.ENGLISH_1A_priedas_InoStartas_en.tab3.tab3 import main3
from code.agents.ENGLISH_1A_priedas_InoStartas_en.tab4.tab4 import main4
from code.agents.ENGLISH_1A_priedas_InoStartas_en.tab5.tab5 import main5
from code.agents.ENGLISH_1A_priedas_InoStartas_en.tab6.tab6 import main6
from code.agents.ENGLISH_1A_priedas_InoStartas_en.tab7.tab7 import main7
from code.agents.ENGLISH_1A_priedas_InoStartas_en.tab8.tab8 import main8
from code.agents.ENGLISH_1A_priedas_InoStartas_en.tab9.tab9 import main9
from code.agents.ENGLISH_1A_priedas_InoStartas_en.tab10.tab10 import main10

from code.merge_sheets import merge_excels_to_subsheets_three

completed_data_file=r"code/finalInput.txt"

def run_with_delay(funcs, data_file_path, delay=30, interval=2):
    for i, fn in enumerate(funcs, 1):
        fn(data_file_path)
        if i % interval == 0 and i != len(funcs):
            print(f"⏳ Waiting {delay} seconds...")
            time.sleep(delay)

def excel_agent_run():
   
    print("\n📝 Processing: Patenting & Commercialization...")
    run_with_delay([
        main_patenting,
        main_commercilisat
    ], completed_data_file)

    sheet_paths = [
        "code/agents/ENGISH_1B_priedas_InoStartas_en/Patenting/1. Fic. amounts (patenting) .xlsx",
        "code/agents/ENGISH_1B_priedas_InoStartas_en/Commercialization/2. Fic. amounts (commercialisat.xlsx", 
        "code/agents/ENGISH_1B_priedas_InoStartas_en/TheStagesofPatenting/the stages of patenting.xlsx",
        "code/agents/ENGISH_1B_priedas_InoStartas_en/References/References.xlsx"
    ]
    merge_excels_to_subsheets_one(sheet_paths, output_path="code/output/ENGISH_1B priedas_InoStartas en.xlsx")

    # Forecast
    print("\n💰 Processing: Revenue Forecast...")
    main_forecast(completed_data_file)

    # Budget forms
    print("\n📋 Processing: Budget Forms...")
    run_with_delay([
        main_budgetary_auth,
        main_nonbudgetary
    ], completed_data_file)
    sheet_paths = [
        "code/agents/ENGISH_Rekomenduojamaforma_en/Certificate_for_Budgetary_Authorization/Certificate_for_budgetary_autho_filled.xlsx",
        "code/agents/ENGISH_Rekomenduojamaforma_en/Other_Non_Budgetary/budgetary_filled.xlsx", 
        "code/agents/ENGISH_Rekomenduojamaforma_en/FN for Holiday Pay/FN for holiday pay.xlsx",
        "code/agents/ENGISH_Rekomenduojamaforma_en/FN for Additional Rest Days/FN for additional rest days .xlsx"
    ]
    merge_excels_to_subsheets_two(sheet_paths, output_path="code/output/engish_rekomenduojama_forma_de_____l_planuojamo_darbo_uz_____mokesc_____io_en.xlsx")

    # 1A tab & data generation
    print("\n📊 Processing: 1A Forms & Data Generation...")
    run_with_delay([
        mainsummary, mainstaff, maindata,
        main1, main2, main3, main4,
        main5, main6, main7, main8,
        main9, main10
    ], completed_data_file)

    sheet_paths = [
        "code/agents/ENGLISH_1A_priedas_InoStartas_en/Summary/Summary.xlsx",
        "code/agents/ENGLISH_1A_priedas_InoStartas_en/Staff/Staff.xlsx", 
        "code/agents/ENGLISH_1A_priedas_InoStartas_en/tab1/1.xlsx",
        "code/agents/ENGLISH_1A_priedas_InoStartas_en/tab2/2.xlsx",
        "code/agents/ENGLISH_1A_priedas_InoStartas_en/tab3/3.xlsx",
        "code/agents/ENGLISH_1A_priedas_InoStartas_en/tab4/4.xlsx",
        "code/agents/ENGLISH_1A_priedas_InoStartas_en/tab5/5.xlsx",
        "code/agents/ENGLISH_1A_priedas_InoStartas_en/tab6/6.xlsx",
        "code/agents/ENGLISH_1A_priedas_InoStartas_en/tab7/7.xlsx",
        "code/agents/ENGLISH_1A_priedas_InoStartas_en/tab8/8.xlsx",
        "code/agents/ENGLISH_1A_priedas_InoStartas_en/tab9/9.xlsx",
        "code/agents/ENGLISH_1A_priedas_InoStartas_en/tab10/10.xlsx",
        "code/agents/ENGLISH_1A_priedas_InoStartas_en/Data/DATA.xlsx"
    ]
    merge_excels_to_subsheets_three(sheet_paths, output_path="code/output/ENGLISH_1A priedas_InoStartas en.xlsx")
    
    print("\n🎉 All processing completed successfully!")
    print("📁 Check the 'output' folder for generated Excel files.")


if __name__ == "__main__":
    excel_agent_run()
