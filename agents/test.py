# {
#   "COMPANY_NAME": "Extract company name",
#   "COMPANY_CODE": "Extract Company code*",
#   "MANAGER_POSITION": "Extract manager position",
#   "MANAGER_NAME": "Extract manager name",
#   "RES_MANA": "NOT_FOUND", 
#   "QUALI": "NOT_FOUND",
#   "COMPLETION_DATE": "Today's date in DD.MM.YYYY format",
#   "MAIN_ACTIVITY": "Extract Main business activity from ECC classification",
#   "ACTIVITY_PERCENTAGE": "Extract Share of activity (%) in total company activity",
#   "EACC_CLASS": "Extract Class of the CESE",
#   "Name_of_the_legal_entity": "Extract Name of the legal entity",
#   "Identification_code": "Extract Identification code",
#   "Shareholding": "Extract Shareholding, %",
#   "A_S_Ns": "Extract Shareholder name",
#   "SHARE_HS": "Extract Shareholding, %",
#   "S_H": "Extract Name of the legal entity",
#   "S_I": "Extract Identification code",
#   "S_S": "Extract Shareholding, %",
#   "MANAGER_TITLE": "Extract manager title",
#   "PERIOD": "Extract Period (year and month) of planned recruitment",
#   "SUMMARY": "Extract and write a 200-250 word summary about your company, your innovative product, its market potential, costs, and future plan.",
#   "PRODUCT_NAME": "Extract product name or use \"NOT_FOUND\"",
#   "PRODUCT_DESCRIPTION": "NOT_FOUND",
#   "JUS_PRO": "Extract justification for product novelty or use \"NOT_FOUND\"",
#   "NOVELTY_LEVEL": "Determine: \"company level\", \"market level\", \"global level\" or \"NOT_FOUND\"",
#   "RD_PRIORITY": "Choose: \"Health technologies\", \"Production processes\", \"Information and communication technologies\" or \"NOT_FOUND\"",
#   "JUS_R_D_I": "Extract how the project matches any R&D&I priority and its theme or use \"NOT_FOUND\"",
#   "RESEARCH_AREA": "Extract research fields or use \"NOT_FOUND\"",
#   "PROJECT_KEYWORDS": "Extract ALL relevant keywords from the text, especially technical terms, separated by commas or use \"NOT_FOUND\"",
#   "PROJECT_LEADER": "NOT_FOUND",
#   "RES_LEA": "NOT_FOUND",
#   "TASK_RES": "NOT_FOUND",
#   "TIME_TAS": "NOT_FOUND",
#   "N_As": "Extract the name of the asset (e.g., premises, equipment, software) used in the R&D activities or use \"NOT_FOUND\"",
#   "F_Os": "Extract the form of ownership for the asset (e.g., owned, leased, shared) or use \"NOT_FOUND\"",
#   "S_Us": "Extract the share or amount of the asset used for R&D (e.g., %, m², number of units) or use \"NOT_FOUND\"",
#   "W_R_Ds": "Extract which R&D activities the asset will be used for or use \"NOT_FOUND\"",
#   "TEAM_SIZE": "NOT_FOUND",
#   "PROJECT_TYPE": "Choose: \"Health technologies and biotechnologies\", \"New production processes, materials and technologies\", \"Information and communication technologies\" or \"NOT_FOUND\"",
#   "PROJECT_SUBTOPIC": "Extract specific subtopic or use \"NOT_FOUND\"",
#   "RD_BUDGET": "Extract Eligible project costs (I), EUR or use \"NOT_FOUND\"",
#   "PROJECT_DURATION": "NOT_FOUND",
#   "REVENUE_PROJECTION": "Extract Planned revenue (P), EUR or use \"NOT_FOUND\"",
#   "REVENUE_RATIO": "Extract Revenue to expenditure ratio (X)* or use \"NOT_FOUND\"",
#   "RD_EXPENDITURE_2022": "Extract R&D expenditure for 2022 or use \"NOT_FOUND\"",
#   "RD_EXPENDITURE_2023": "Extract R&D expenditure for 2023 or use \"NOT_FOUND\"",
#   "PRODUCT_PRICE": "NOT_FOUND",
#   "PRICE_JUSTIFICATION": "NOT_FOUND",
#   "CURRENT_TPL": "Extract current Technology Readiness Level or use \"NOT_FOUND\"",
#   "TARGET_TPL": "Extract target Technology Readiness Level or use \"NOT_FOUND\"",
#   "TPL_JUSTIFICATION": "Extract TPL justification or use \"NOT_FOUND\"",
#   "PROJECT_IMPACT_TITLE": "Extract project impact title or use \"NOT_FOUND\"",
#   "PROJECT_START_MONTH": "Extract project start month or use \"NOT_FOUND\"",
#   "PROJECT_COMPLETION_MONTH": "Extract project completion month or use \"NOT_FOUND\"",
#   "START_TPL_IMPACT": "NOT_FOUND",
#   "END_TPL_IMPACT": "NOT_FOUND",
#   "PROJECT_IMPACT_DESCRIPTION": "Extract detailed project impact description or use \"NOT_FOUND\"",
#   "COMPETITOR_1": "Extract main competitor name or use \"NOT_FOUND\"",
#   "COMPETITOR_MARKET_SHARE": "Extract market share percentage or use \"NOT_FOUND\"",
#   "TOTAL_RESEARCH_JOBS": "Extract total research jobs or use \"NOT_FOUND\"",
#   "JOBS_DURING_PROJECT": "Extract jobs during project or use \"NOT_FOUND\"",
#   "JOBS_AFTER_PROJECT": "Extract jobs after project or use \"NOT_FOUND\"",
#   "RISK_STAGE_1": "Extract first risk stage/phase or use \"NOT_FOUND\"",
#   "RISK_DESCRIPTION_1": "Extract first risk description or use \"NOT_FOUND\"",
#   "CRITICAL_POINT_1": "Extract first critical point or use \"NOT_FOUND\"",
#   "MITIGATION_ACTION_1": "Extract first mitigation action or use \"NOT_FOUND\"",
#   "RISK_STAGE_2": "Extract second risk stage/phase or use \"NOT_FOUND\"",
#   "RISK_DESCRIPTION_2": "Extract second risk description or use \"NOT_FOUND\"",
#   "CRITICAL_POINT_2": "Extract second critical point or use \"NOT_FOUND\"",
#   "MITIGATION_ACTION_2": "Extract second mitigation action or use \"NOT_FOUND\"",
#   "RISK_STAGE_3": "Extract third risk stage/phase or use \"NOT_FOUND\"",
#   "RISK_DESCRIPTION_3": "Extract third risk description or use \"NOT_FOUND\"",
#   "CRITICAL_POINT_3": "Extract third critical point or use \"NOT_FOUND\"",
#   "MITIGATION_ACTION_3": "Extract third mitigation action or use \"NOT_FOUND\"",
#   "RISK_STAGE_4": "Extract fourth risk stage/phase or use \"NOT_FOUND\"",
#   "RISK_DESCRIPTION_4": "Extract fourth risk description or use \"NOT_FOUND\"",
#   "CRITICAL_POINT_4": "Extract fourth critical point or use \"NOT_FOUND\"",
#   "MITIGATION_ACTION_4": "Extract fourth mitigation action or use \"NOT_FOUND\""
# }







class Solution(object):
    def numSquarefulPerms(self, A):
        ret = []
        self.dfs(sorted(A), [], ret)
        return len(ret)
    
    def dfs(self, nums, path, ret):
        if not nums:
            ret.append(path)
        for i in range(len(nums)):
            if i > 0 and nums[i] == nums[i-1]:
                continue # skip duplicates
            if path and not self.square(path[-1]+nums[i]):
                continue # backtracking without going further 
            self.dfs(nums[:i]+nums[i+1:], path+[nums[i]], ret)
        
    def square(self, num):
        from math import sqrt
        return pow(int(sqrt(num)), 2) == num