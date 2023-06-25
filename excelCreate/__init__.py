import openpyxl


class Create_Excel:

    def __init__(self, wb):
        self.wb = openpyxl.load_workbook(wb)

    def naver_sa_write(self, sheet, data, cellNo):

        selected_sheet = self.wb[sheet]

        for idx, i in enumerate(data):
            imps_data = data[idx]['data'][0]['impCnt']
            clicks_data = data[idx]['data'][0]['clkCnt']
            cost_data = data[idx]['data'][0]['salesAmt']
            ccnt_data = data[idx]['data'][0]['ccnt']
            convAmt_data = data[idx]['data'][0]['convAmt']

            selected_sheet['C'+str(cellNo)] = imps_data
            selected_sheet['D'+str(cellNo)] = clicks_data
            selected_sheet['G'+str(cellNo)] = cost_data
            selected_sheet['H'+str(cellNo)] = ccnt_data
            selected_sheet['K'+str(cellNo)] = convAmt_data

            cellNo += 1

    def naver_brand_sa_write(self, sheet, data, cellNo, cost):

        selected_sheet = self.wb[sheet]

        for idx, i in enumerate(data):
            imps_data = data[idx]['data'][0]['impCnt']
            clicks_data = data[idx]['data'][0]['clkCnt']
            # cost_data = data[idx]['data'][0]['salesAmt']
            ccnt_data = data[idx]['data'][0]['ccnt']
            convAmt_data = data[idx]['data'][0]['convAmt']

            selected_sheet['C'+str(cellNo)] = imps_data
            selected_sheet['D'+str(cellNo)] = clicks_data
            selected_sheet['G'+str(cellNo)] = cost
            selected_sheet['H'+str(cellNo)] = ccnt_data
            selected_sheet['K'+str(cellNo)] = convAmt_data

            cellNo += 1

    def google_ads_write(self, sheet, data, cellNo):

        selected_sheet = self.wb[sheet]

        for idx, i in enumerate(data['impCnt']):
            imps_data = data['impCnt'][idx]
            clicks_data = data['clkCnt'][idx]
            cost_data = data['salesAmt'][idx] * data['clkCnt'][idx]
            ccnt_data = data['ccnt'][idx]
            convAmt_data = data['convAmt'][idx]

            selected_sheet['C'+str(cellNo)] = imps_data
            selected_sheet['D'+str(cellNo)] = clicks_data
            selected_sheet['N'+str(cellNo)] = cost_data
            selected_sheet['H'+str(cellNo)] = ccnt_data
            selected_sheet['K'+str(cellNo)] = convAmt_data

            cellNo += 1

    def tg_write(self):

        for idx, i in enumerate(impression_cnt):
            imps_data = impression_cnt[idx]
            clicks_data = click_cnt[idx]
            adCost_data = ad_cost[idx]
            ccnt_data = conversion_cnt[idx]
            convAmt_data = total_basket_value[idx]

            ws_tg['D'+str(tg_cell_count)] = imps_data
            ws_tg['E'+str(tg_cell_count)] = clicks_data
            ws_tg['H'+str(tg_cell_count)] = adCost_data
            ws_tg['I'+str(tg_cell_count)] = ccnt_data
            ws_tg['K'+str(tg_cell_count)] = convAmt_data

            tg_cell_count += 1

    def save(self, report_name):
        self.wb.save(report_name)
        self.wb.close()
