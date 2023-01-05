import requests
import csv
import sys
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from orkut.settings import WARRANTY_BASE_URL
import logging

all_test=logging.getLogger('all')
cd_ew_test=logging.getLogger('cd_ew')
cd_croma_test=logging.getLogger('cd_croma')
cd_dg_test=logging.getLogger('cd_dg')
cd_ola_test=logging.getLogger('cd_ola')
xiaomi_tv_test=logging.getLogger('xiaomi_tv')
xiaomi_others_test=logging.getLogger('xiaomi_others')
mobile_croma_test=logging.getLogger('mobile_croma')
mobile_mi_test=logging.getLogger('mobile_mi')
mobile_ew_test=logging.getLogger('mobile_ew')
mobile_dg_test=logging.getLogger('mobile_dg')
lifestyle_test=logging.getLogger('lifestyle')
rem_test=logging.getLogger('rem')



class AutoReport:

    agent_codes=[]
    context={}
    complete_data=[]
    ac_list=['air conditioner','split ac','window ac']
    whatsapp_code='99679'
    # ------------------------------------------------------------------------------------------------------------

    def get_calls_data(self,start_date,end_date):

        url = "https://crm-apis.zopper.com/call/claims/listing?from={start_date}&to={end_date}".format(start_date=start_date,end_date=end_date)
        payload={}
        headers = {
        'authority': 'crm-apis.zopper.com',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'authorization': 'Token 84fd947069c66347c644d57a1e8c9f159c1776c9',
        'content-type': 'application/json',
        'origin': 'https://service-crm.zopper.com',
        'referer': 'https://service-crm.zopper.com/',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }

        print("https://crm-apis.zopper.com/call/claims/listing?from={start_date}&to={end_date}".format(start_date=start_date,end_date=end_date))

        response = requests.request("GET", url, headers=headers, data=payload)

        return (response.json().get('data').get('results'))

    def initiate_calls_data(self,start_date=datetime.now().replace(day=1).date(),end_date=datetime.now().date()):

        start_date=datetime.now().replace(day=1).date()
        end_date=datetime.now().replace(day=3).date()

        l=[]
        c=[]

        days=(end_date-start_date).days+1

        print(days)

        gap=10

        

        while days>gap :

            c=self.get_calls_data(start_date,start_date+relativedelta(days=gap-1))
            l=l+c
            start_date=start_date+relativedelta(days=gap)
            days=days-gap

        else:

            c=self.get_calls_data(start_date,end_date)
            l=l+c


        return l

    def latest_month_report(self):

        ola_count=0
        ew_count = 0                                                                                                                                                                
        croma_count = 0  
        cd_dg=0
        mi_mobile_count = 0
        mi_tv_count = 0
        mi_others_count = 0                                                                                                                                                                                                                                                                                                                  
        mobile_count = 0                                                                                                                                                            
        others_fur_cycle_specs_count = 0 
        mob_ew=0
        mobile_dg=0
        mobile_count_croma=0
        calls_data=[]
        # --------------------
        warranty_type=''
        item_category_id=0
        display_name=''
        cd_dd=0
        cd_iifl_dg=0
        cd_iifl_dg_pro=0
        cd_sang_dg_pro=0
        mob_dd=0
        mob_iifl_dg=0
        mob_iifl_dg_pro=0
        mob_sang_dg_pro=0
        
        res = requests.get(WARRANTY_BASE_URL+'/zopper/documents?code=crm-report-config').json()
        config = res.get('data')

        res = requests.get(WARRANTY_BASE_URL+'/zopper/documents?code=mi_config').json()
        mi_config = res.get('data')
        
        
        
        
        
        croma_channel = config.get('CROMA_CHANNEL')

        MOB_EW=('ADLD'.upper(),'Cashify'.upper(),'EW ADLD'.upper(),'Mobile EW'.upper(),'New warranty Kit'.upper(),'Warranty Kit'.upper(),'Zed Secure'.upper())
        MOB_CROMA=("Device Secure Gold".upper(), "Device Secure".upper(), "On Demand Service".upper(), "Screen Protection".upper())
        MOB_DG=('device doctor'.upper(),'iifl device genie'.upper(),'iifl device genie pro'.upper(),'sangeetha device genie'.upper())
        CD_CROMA=("Device Secure Gold".upper(), "Device Secure".upper(), "On Demand Service".upper(), "Screen Protection".upper(), 'HOME ASSURE'.upper())
        CD_DG=('device doctor'.upper(),'iifl device genie'.upper(),'iifl device genie pro'.upper(),'sangeetha device genie'.upper())
        CD_OLA=('Ola Home Device Protect'.upper())




        # CYCLE_CATEGORY FURNITURE_CATEGORY SPECS_CATEGORY
        CYCLE_CATEGORY = config.get('CYCLE_CATEGORY')
        FURNITURE_CATEGORY = config.get('FURNITURE_CATEGORY')
        SPECS_CATEGORY = config.get('SPECS_CATEGORY')
        MOBILE_CATEGORIES = [config.get('MOBILE_CATEGORY')]
        MI_MOBILE_CATEGORIES = mi_config.get('mi_mobile_categories')
        MI_TV_CATEGORIES = mi_config.get('categories')
        MI_OTHERS_CATEGORIES = config.get('Mi_Other_category')+mi_config.get('mi_laptop_categories')+mi_config.get('mi_purifier_categories')+mi_config.get('vaccum_cleaner_categories')

        # ALL NON_CD CATEGORIES
        NON_CD_CATEGORIES = MI_TV_CATEGORIES + MI_OTHERS_CATEGORIES + [CYCLE_CATEGORY , FURNITURE_CATEGORY , SPECS_CATEGORY]
        device_genie_data = {}
        display_names = set()
        croma_business_list=[]
        croma_business_list =[]
        print('croma_business_list --> ',croma_business_list)
        
        calls_data=self.initiate_calls_data()


        for data in calls_data:
            i=0
            i+=1

            warranty_type=data.get('warranty_type')
            display_name=data.get('display_name')
            item_category_id=data.get('item_category_id')
            item_name=data.get('item_name')

            msg=str(display_name)+"  "+str(warranty_type)+"  "+str(item_category_id)+"  "+str(item_name)

            all_test.error(i+'--> ' + msg)


            if item_category_id and item_category_id in (MI_TV_CATEGORIES):
                mi_tv_count += 1
                xiaomi_tv_test.error(msg)

            elif item_category_id and item_category_id in (MI_OTHERS_CATEGORIES):
                mi_others_count += 1
                xiaomi_others_test.error(msg)

            elif item_category_id and item_category_id in (CYCLE_CATEGORY , FURNITURE_CATEGORY , SPECS_CATEGORY):
                others_fur_cycle_specs_count += 1
                lifestyle_test.error(msg)

            elif item_category_id and item_category_id in (MI_MOBILE_CATEGORIES):
                mi_mobile_count += 1
                mobile_mi_test.error(msg)

            elif item_category_id and item_category_id in (MOBILE_CATEGORIES):

                if display_name and display_name.upper() in MOB_CROMA :

                    if  data.get('item_serial_number') and data.get('item_serial_number')!='':
                        mobile_count_croma += 1
                        mobile_croma_test.error(msg)

                    else:
                        rem_test.error(msg)


                elif display_name and display_name.upper() in MOB_DG :
                    mobile_dg += 1
                    mobile_dg_test.error(msg)

                else:
                    mob_ew += 1
                    mobile_ew_test.error(msg)

            elif display_name and display_name.upper() in CD_CROMA:
                croma_count += 1
                cd_croma_test.error(msg)

            elif display_name and display_name.upper() in CD_DG:
                cd_dg += 1
                cd_dg_test.error(msg)

            elif display_name and display_name.upper() in CD_OLA:
                ola_count += 1
                cd_ola_test.error(msg)

            else:
                ew_count += 1
                cd_ew_test.error(msg)

            # -----------------------------------------------------------------

            if display_name and display_name.upper() == 'device doctor'.upper():

                if item_category_id and item_category_id in (MI_MOBILE_CATEGORIES + MOBILE_CATEGORIES):

                    mob_dd+=1
                    # all_test.error(msg)

                elif item_category_id and item_category_id not in NON_CD_CATEGORIES:

                    cd_dd+=1
                    # all_test.error(msg)

            elif display_name and display_name.upper() == 'iifl device genie'.upper():

                if item_category_id and item_category_id in (MI_MOBILE_CATEGORIES + MOBILE_CATEGORIES):

                    mob_iifl_dg+=1
                    # all_test.error(msg)

                elif item_category_id and item_category_id not in NON_CD_CATEGORIES:

                    cd_iifl_dg+=1
                    # all_test.error(msg)

            elif display_name and display_name.upper() == 'iifl device genie pro'.upper():

                if item_category_id and item_category_id in (MI_MOBILE_CATEGORIES + MOBILE_CATEGORIES):

                    mob_iifl_dg_pro+=1
                    # all_test.error(msg)

                elif item_category_id and item_category_id not in NON_CD_CATEGORIES:

                    cd_iifl_dg_pro+=1
                    # all_test.error(msg)

            elif display_name and display_name.upper() == 'sangeetha device genie'.upper():

                if item_category_id and item_category_id in (MI_MOBILE_CATEGORIES + MOBILE_CATEGORIES):

                    mob_sang_dg_pro+=1
                    # all_test.error(msg)

                elif item_category_id and item_category_id not in NON_CD_CATEGORIES:

                    cd_sang_dg_pro+=1
                    # all_test.error(msg)





        
        print("mi_tv_count --> ",mi_tv_count)
        print("mi_others_count --> ",mi_others_count)
        print("others_fur_cycle_specs_count --> ",others_fur_cycle_specs_count)
        print("mi_mobile_count --> ",mi_mobile_count)
        print("mob_ew --> ",mob_ew)
        print("mobile_count_croma --> ",mobile_count_croma)
        print("mobile_dg --> ",mobile_dg)
        print("CD ew_count --> ",ew_count)
        print("CD croma_count --> ",croma_count)
        print("CD cd_dg --> ",cd_dg)
        print("CD ola_count --> ",ola_count)

        print("Device doctor --> " ,cd_dd," ",mob_dd)
        print("IIFL DG--> ",cd_iifl_dg," ",mob_iifl_dg)
        print("IIFL DG PRO --> ",cd_iifl_dg_pro,' ',mob_iifl_dg_pro)
        print("S DG PRO --> ",cd_sang_dg_pro," ",mob_sang_dg_pro)



     
                    
                    


a=AutoReport()                                                                                                                     

a.latest_month_report() 
