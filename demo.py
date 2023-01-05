import requests
import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta
import csv
from django.core.mail import send_mail
from django.template import loader
from django.conf import settings
# import sys
# from os.path import exists
# import json


class AutoReport:
    complete_data=[]
    cd=['air conditioner','air cooler','air purifier','chimney','desktop','dish washer','dvd & blu-ray player','electric kettle','fan','food maker','geyser','hair dryer','headphones','home theater','induction cooker','iron','laptop','lcd/led tv','microwave oven','mixer, juicer, grinder','otg','printer','refrigerator','room heater','small appliances','smart watch','speakers','split ac','television','toaster','tv & home entertainment','unknown','vacuum cleaner','washing machine','water dispenser','water purifier','window ac']
    mob_ew_list=['warranty kit', 'new warranty kit', 'assure', 'zopper assure']
    mob_croma_list=['device secure gold', 'device secure', 'on demand service', 'screen protection']
    mob_dg_list=['device doctor','iifl device genie','iifl device genie pro','sangeetha device genie']
    mob_ola_list=['ola home device protect']
    cd_ew_list=['warranty kit', 'new warranty kit', 'assure', 'zopper assure']
    cd_croma_list=['device secure gold', 'device secure', 'on demand service', 'home assure', 'screen protection']
    cd_dg_list=['device doctor','iifl device genie','iifl device genie pro','sangeetha device genie']
    cd_ola_list=['ola home device protect']
    lifestyle_list=['spectacles', 'furniture', 'cycle', 'watch', 'gym equipment']
    xiaomi_tv_list=['mi led tv (32")','mi led tv (43")','mi led tv (55")','mi led tv 4a (40")','mi led tv 4x (43")','mi led tv 4x (50")','mi led tv 4x (65")','mi tv q1 189.34cm 75inch','mitv 4a horizon edition 40 inch','mi tv 5x 43','mi tv 5x 50','mi tv horizon (32")','mi tv horizon (43")','mi tv q1(55")','redmi smart tv 32','redmi smart tv 43','redmi smart tv x50','redmi smart tv x55','redmi smart tv x65']
    xiaomi_others_list=['mi notebook 14 horizon (8gb ram + 512gb nvme ssd, i7 10th gen + nvidia mx350)','mi notebook 14 horizon (8gb ram + 512gb ssd, i5 10th gen + nvidia mx350)','mi robot vacuum-mop p','mi water purifier']
    plan_name=['device doctor','iifl device genie','iifl device genie pro','sangeetha device genie']
    agent_codes=['34440','35366','89535','37592','34435','99355','73948','34021','40225','40347','83330','73201','74404','89591','34444','88264','35365','37593','110194','89590','95030','60017','74527','74525','67094','36596','67461','82236','36096','36018','97457','91559','82128','63023','96941','110192','37595','62195','37594','101202']
    ac_list=['air conditioner','split ac','window ac']
    whatsapp_code='99679'

    def get_mobile_plan_wise(self,data):

        planswise_mobile_list=[0,0,0,0]

        for list in data:
            if list[32].lower() == 'mobile':

                if list[49].lower() in self.mob_croma_list:
                    planswise_mobile_list[0]+=1

                elif list[49].lower() in self.mob_ew_list:
                    planswise_mobile_list[1]+=1

                elif list[49].lower() in self.mob_dg_list:
                    planswise_mobile_list[2]+=1

                elif list[49].lower() in self.mob_ola_list:
                    planswise_mobile_list[3]+=1

    
    def get_last_month_cd_plan_wise(self,data):

        planswise_cd_list=[0,0,0,0]

        for list in data:

            if list[32].lower() in self.cd:

                if list[49].lower() in self.cd_ew_list:
                    planswise_cd_list[0]+=1

                elif list[49].lower() in self.cd_croma_list:
                    planswise_cd_list[1]+=1

                elif list[49].lower() in self.cd_dg_list:
                    planswise_cd_list[2]+=1

                elif list[49].lower() in self.cd_ola_list:
                    planswise_cd_list[3]+=1

        return planswise_cd_list



    def get_lifestyle_cd_item_category(self,data):
        lifestyle_count=0

        for list in data:
            if list[32].lower() in self.lifestyle_list:
                
                lifestyle_count+=1

        return lifestyle_count

    def get_xiaomi_items(self,data):
        
        xiaomi_tv_count=0
        xiaomi_others_count=0

        for list in data:
            if list[32].lower() in self.xiaomi_tv_list:

                xiaomi_tv_count+=1

            elif list[32].lower() in self.xiaomi_others_list:

                xiaomi_others_count+=1

        return xiaomi_tv_count,xiaomi_others_count



    def get_cd_mobile(self,data):

        cd_count=[0,0,0,0]
        mobile_count=[0,0,0,0]
        for list in data:
            if list[49].lower() == self.plan_name[0]:
                if list[32].lower() in self.cd:
                    cd_count[0]+=1
                elif list[32].lower() == 'mobile':
                    mobile_count[0]+=1

            elif list[49].lower() == self.plan_name[1]:
                if list[32].lower() in self.cd:
                    cd_count[1]+=1
                elif list[32].lower() == 'mobile':
                    mobile_count[1]+=1

            elif list[49].lower() == self.plan_name[2]:
                if list[32].lower() in self.cd:
                    cd_count[2]+=1
                elif list[32].lower() == 'mobile':
                    mobile_count[2]+=1

            elif list[49].lower() == self.plan_name[3]:
                if list[32].lower() in self.cd:
                    cd_count[3]+=1
                elif list[32].lower() == 'mobile':
                    mobile_count[3]+=1

        return cd_count,mobile_count



    def claim_raised(self,data):
        wa_claims=0
        za_claims=0

        for list in data:
            if list[10]==self.whatsapp_code:
               wa_claims+=1

            elif list[10] not in self.agent_codes:
                za_claims+=1

        return (wa_claims,za_claims)


    def all_claims_count(self,data):
        return len(data)

    def start_process(self,start_date,end_date):
        print("start date --> {} , end date --> {}".format(start_date,end_date))
        try:
            data=[]
            return data
        except Exception as e:
            print(e)
            

    def get_dates(self,date):

        last_date_curr_month=datetime.now().replace(day=1).date()+relativedelta(days=-1,months=1)
        start_date=datetime.strptime(date,"%Y-%m-%d").date()
        # calculating the last date of current month
        last_date=start_date+relativedelta(days=-1,months=1)

        # dividing current month into 3 segments of 10 days
        if last_date <= last_date_curr_month:
            monthly_data=[]
            next_date=start_date+relativedelta(days=9)
            d1=self.start_process(start_date,next_date)
            start_date=next_date+relativedelta(days=1)
            next_date=start_date+relativedelta(days=9)
            d2=self.start_process(start_date,next_date)
            start_date=next_date+relativedelta(days=1)
            d3=self.start_process(start_date,last_date)
            monthly_data=d1+d2+d3
            self.complete_data.append(monthly_data)

    # getting count of ON-DEMAND-SERVICE(ODS) and AC under ODS
    def get_data_od(self,data):

        od_claims=0
        od_ac_claims=0

        for lt in data:
            if lt[49].lower()=='on demand service':
                od_claims+=1

                if lt[32].lower() in self.ac_list:
                    od_ac_claims+=1

        return(od_claims,od_ac_claims)



    # getting claim_data for a particular start and end date 
    def get_data(self,start_date,end_date):

            url = "https://crm-apis.zopper.com/call/claims/listing/download?from={start_date}&to={end_date}".format(start_date=start_date,end_date=end_date)

            payload={}
            headers = {
                'authority': 'crm-apis.zopper.com',
                'sec-ch-ua': '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
                'accept': 'application/json, text/plain, */*',
                'content-type': 'application/json',
                'authorization': 'Token 190b23d27e3036e1d82125c60d8773e2d73009f8',
                'sec-ch-ua-mobile': '?0',
                'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
                'sec-ch-ua-platform': '"macOS"',
                'origin': 'https://service-crm.zopper.com',
                'sec-fetch-site': 'same-site',
                'sec-fetch-mode': 'cors',
                'sec-fetch-dest': 'empty',
                'referer': 'https://service-crm.zopper.com/',
                'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'
            }

            response = requests.request("GET", url, headers=headers, data=payload)
            decoded_content = response.content.decode('utf-8')

            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)

            return my_list[1:]


    def __init__(self):

        od_claims_list=[]
        od_ac_claims_list=[]
        all_claims_count_list=[]
        wa_claims_list=[]
        za_claims_list=[]
        ce_claims_list=[]
        total_cd_mobile_claims=[]
        total_cd=0
        total_mobile=0
        grand_total=0
        last_month_cd_plan_wise=[]
        xiaomi_tv=0
        xiaomi_others=0
        lifestyle=0
        monthlist=[]
        email_attachment_template_context={}
        planswise_mobile_list=[]

        try:
            # Calculating 12 dates for past 12 months starting from 1st of every month
            monthlist.append(str(datetime.now().replace(day=1).date() - relativedelta(months=11)))
            monthlist.append(str(datetime.now().replace(day=1).date() - relativedelta(months=10)))
            monthlist.append(str(datetime.now().replace(day=1).date() - relativedelta(months=9)))
            monthlist.append(str(datetime.now().replace(day=1).date() - relativedelta(months=8)))
            monthlist.append(str(datetime.now().replace(day=1).date() - relativedelta(months=7)))
            monthlist.append(str(datetime.now().replace(day=1).date() - relativedelta(months=6)))
            monthlist.append(str(datetime.now().replace(day=1).date() - relativedelta(months=5)))
            monthlist.append(str(datetime.now().replace(day=1).date() - relativedelta(months=4)))
            monthlist.append(str(datetime.now().replace(day=1).date() - relativedelta(months=3)))
            monthlist.append(str(datetime.now().replace(day=1).date() - relativedelta(months=2)))
            monthlist.append(str(datetime.now().replace(day=1).date() - relativedelta(months=1)))
            monthlist.append(str(datetime.now().replace(day=1).date()))

            print(monthlist)

            email_attachment_template_context={
                "m1":datetime.strptime(monthlist[0],"%Y-%m-%d").strftime("%B-%Y"),
                "m2":datetime.strptime(monthlist[1],"%Y-%m-%d").strftime("%B-%Y"),
                "m3":datetime.strptime(monthlist[2],"%Y-%m-%d").strftime("%B-%Y"),
                "m4":datetime.strptime(monthlist[3],"%Y-%m-%d").strftime("%B-%Y"),
                "m5":datetime.strptime(monthlist[4],"%Y-%m-%d").strftime("%B-%Y"),
                "m6":datetime.strptime(monthlist[5],"%Y-%m-%d").strftime("%B-%Y"),
                "m7":datetime.strptime(monthlist[6],"%Y-%m-%d").strftime("%B-%Y"),
                "m8":datetime.strptime(monthlist[7],"%Y-%m-%d").strftime("%B-%Y"),
                "m9":datetime.strptime(monthlist[8],"%Y-%m-%d").strftime("%B-%Y"),
                "m10":datetime.strptime(monthlist[9],"%Y-%m-%d").strftime("%B-%Y"),
                "m11":datetime.strptime(monthlist[10],"%Y-%m-%d").strftime("%B-%Y"),
                "m12":datetime.strptime(monthlist[11],"%Y-%m-%d").strftime("%B-%Y"),
                "cd_ew":last_month_cd_plan_wise[0],
                "cd_croma":last_month_cd_plan_wise[1],
                "cd_dg":last_month_cd_plan_wise[2],
                "cd_ohd":last_month_cd_plan_wise[3],
                "total_cd":sum(last_month_cd_plan_wise),
                "mi_tv":xiaomi_tv,
                "mi_others":xiaomi_others,
                "mob_croma":planswise_mobile_list[0],
                "mob_mi":planswise_mobile_list[1],
                "mob_ew":planswise_mobile_list[2],
                "mob_dg":planswise_mobile_list[3],
                "ls":lifestyle,
                "ce":sum(za_claims_list)-za_claims_list[-1],
                "total_wa":sum(wa_claims_list)-wa_claims_list[-1],
                "total_ce":sum(ce_claims_list)-ce_claims_list[-1],
                "mon_od_1":od_claims_list[0],
                "mon_od_2":od_claims_list[1],
                "mon_od_3":od_claims_list[2],
                "mon_od_4":od_claims_list[3],
                "mon_od_5":od_claims_list[4],
                "mon_od_6":od_claims_list[5],
                "mon_od_7":od_claims_list[6],
                "mon_od_8":od_claims_list[7],
                "mon_od_9":od_claims_list[8],
                "mon_od_10":od_claims_list[9],
                "mon_od_11":od_claims_list[10],
                "mon_od_12":od_claims_list[11],
                "tot_od":sum(od_claims_list),
                "mon_od_ac_1":od_ac_claims_list[0],
                "mon_od_ac_2":od_ac_claims_list[1],
                "mon_od_ac_3":od_ac_claims_list[2],
                "mon_od_ac_4":od_ac_claims_list[3],
                "mon_od_ac_5":od_ac_claims_list[4],
                "mon_od_ac_6":od_ac_claims_list[5],
                "mon_od_ac_7":od_ac_claims_list[6],
                "mon_od_ac_8":od_ac_claims_list[7],
                "mon_od_ac_9":od_ac_claims_list[8],
                "mon_od_ac_10":od_ac_claims_list[9],
                "mon_od_ac_11":od_ac_claims_list[10],
                "mon_od_ac_12":od_ac_claims_list[11],
                "tot_ac":sum(od_ac_claims_list),
                "m1_tc":all_claims_count_list[0],
                "m2_tc":all_claims_count_list[1],
                "m3_tc":all_claims_count_list[2],
                "m4_tc":all_claims_count_list[3],
                "m5_tc":all_claims_count_list[4],
                "m6_tc":all_claims_count_list[5],
                "m7_tc":all_claims_count_list[6],
                "m8_tc":all_claims_count_list[7],
                "m9_tc":all_claims_count_list[8],
                "m10_tc":all_claims_count_list[9],
                "m11_tc":all_claims_count_list[10],
                "m_tc":sum(all_claims_count_list)-all_claims_count_list[-1],
                "mon_za_1":za_claims_list[0],
                "mon_za_2":za_claims_list[1],
                "mon_za_3":za_claims_list[2],
                "mon_za_4":za_claims_list[3],
                "mon_za_5":za_claims_list[4],
                "mon_za_6":za_claims_list[5],
                "mon_za_7":za_claims_list[6],
                "mon_za_8":za_claims_list[7],
                "mon_za_9":za_claims_list[8],
                "mon_za_10":za_claims_list[9],
                "mon_za_11":za_claims_list[10],
                "mon_za_12":za_claims_list[11],
                "mon_wa_1":wa_claims_list[0],
                "mon_wa_2":wa_claims_list[1],
                "mon_wa_3":wa_claims_list[2],
                "mon_wa_4":wa_claims_list[3],
                "mon_wa_5":wa_claims_list[4],
                "mon_wa_6":wa_claims_list[5],
                "mon_wa_7":wa_claims_list[6],
                "mon_wa_8":wa_claims_list[7],
                "mon_wa_9":wa_claims_list[8],
                "mon_wa_10":wa_claims_list[9],
                "mon_wa_11":wa_claims_list[10],
                "mon_wa_12":wa_claims_list[11],
                "mon_ce_1":ce_claims_list[0],
                "mon_ce_2":ce_claims_list[1],
                "mon_ce_3":ce_claims_list[2],
                "mon_ce_4":ce_claims_list[3],
                "mon_ce_5":ce_claims_list[4],
                "mon_ce_6":ce_claims_list[5],
                "mon_ce_7":ce_claims_list[6],
                "mon_ce_8":ce_claims_list[7],
                "mon_ce_9":ce_claims_list[8],
                "mon_ce_10":ce_claims_list[9],
                "mon_ce_11":ce_claims_list[10],
                "mon_ce_12":ce_claims_list[11],
                "cd_dd":last_month_cd_plan_wise[0],
                "cd_dg":last_month_cd_plan_wise[1],
                "cd_dgp":last_month_cd_plan_wise[2],
                "cd_sdg":last_month_cd_plan_wise[3],
                "mob_dd":planswise_mobile_list[0],
                "mob_dg":planswise_mobile_list[1],
                "mob_dgp":planswise_mobile_list[2],
                "mob_sdg":planswise_mobile_list[3],
            }
            

        except Exception as e:
            print(e)

        try:
            # sending 1 month to be divided into 3 segments of 10 days
            for i in range(0,len(monthlist)):
                self.get_dates(monthlist[i])
            
        except Exception as e:
            print(e)

        try:
            # # getting od claims and od ac claims count
            for lt in self.complete_data:
                od_claims,od_ac_claims=self.get_data_od(lt)
                od_claims_list.append(od_claims)
                od_ac_claims_list.append(od_ac_claims)
            
        except Exception as e:
            print(e)

        try:
            # # getting all claims count
            for lt in self.complete_data:
                count=self.all_claims_count(lt)
                all_claims_count_list.append(count)
            
        except Exception as e:
            print(e)

        try:
            # # calculating count of claims raised by Whatsapp and Zopper app
            for lt in self.complete_data:
                wa_claims,za_claims=self.claim_raised(lt)
                wa_claims_list.append(wa_claims)
                za_claims_list.append(za_claims)

        except Exception as e:
            print(e)

        try:
            # # calculating count of claims raised by customer executives
            for i in range(len(all_claims_count_list)):
                count=all_claims_count_list[i]-wa_claims_list[i]-za_claims_list[i]
                ce_claims_list.append(count)

        except Exception as e:
            print(e)

        try:
            # getting count of CD and Mobile for last month
            cd_count,mobile_count=self.get_cd_mobile(self.complete_data[-1])

        except Exception as e:
            print(e)

        try:
            # getting summation of all cd and mobile claims
            for i in range(len(cd_count)):
                count=cd_count[i]+mobile_count[i]
                total_cd_mobile_claims.append(count)
                total_cd+=cd_count[i]
                total_mobile+=mobile_count[i]
            grand_total=total_cd+total_mobile    

        except Exception as e:
            print(e)

        try:
            # getting xiaomi_tv and xiaomi_others product count 
            xiaomi_tv,xiaomi_others=self.get_xiaomi_items(self.complete_data[-1])

        except Exception as e:
            print(e)

        try:
            # getting lifestyle product count
            lifestyle=self.get_lifestyle_cd_item_category(self.complete_data[-1])

        except Exception as e:
            print(e)

        try:
            # getting CD EW, CROMA, DEVICE GENIE, OLA HOME DEVICE product count
            last_month_cd_plan_wise=self.get_last_month_cd_plan_wise(self.complete_data[-1])

        except Exception as e:
            print(e)


        print("-----------------OD Claims List-----------------")
        print(od_claims_list)
        print("-----------------OD AC Claims List-----------------")
        print(od_ac_claims_list)
        print("-----------------All Claims Count-----------------")
        print(all_claims_count_list)
        print("-----------------WA Claims Raised-----------------")
        print(wa_claims_list)
        print("-----------------ZA Claims Raised-----------------")
        print(za_claims_list)
        print("-----------------CE Claims Raised-----------------")
        print(ce_claims_list)
        print("-----------------CD Claims Raised for last month for 4 Plans-----------------")
        print(cd_count)
        print("-----------------Mobile Claims Raised for last month for 4 Plans-----------------")
        print(mobile_count)
        print("-----------------Summation of CD and Mobile for last month for 4 Plans-----------------")
        print(total_cd_mobile_claims)
        print("-----------------Total of CD Claims Raised for last month for 4 Plans-----------------")
        print(total_cd)
        print("-----------------Total of Mobile Claims Raised for last month for 4 Plans-----------------")
        print(total_mobile)
        print("-----------------Grand Total for last month for 4 Plans-----------------")
        print(grand_total)
        print("-----------------Xiaomi TV Claims Raised for last month for 4 Plans-----------------")
        print(xiaomi_tv)
        print("-----------------Xiaomi Others Claims Raised for last month for 4 Plans-----------------")
        print(xiaomi_others)
        print("-----------------LIFESTYLE Claims Raised for last month-----------------")
        print(lifestyle)
        print("-----------------Total of CD Claims Raised for last month for 4 Plans-----------------")
        print(last_month_cd_plan_wise)



        # email_subject = "Claim Report for {}".format(datetime.today().strftime('%d %b %Y'))
        # email_from = settings.EMAIL_HOST_USER
        # ATTACHMENT_TEMPLATE = 'email.html'
        # rendered_html = loader.get_template(ATTACHMENT_TEMPLATE).render(email_attachment_template_context)
        # email_recipients = ['yash.yadav@zopper.com','yashu.deepyadav@gmail.com']
        # email = EmailMultiAlternatives(email_subject, " ", email_from, email_recipients)
        # email.attach_alternative(rendered_html, 'text/html')
        # status = email.send()
        # print('Email Status : ', status)

        # send_mail(
        #     email_subject = "Claim Report for {}".format(datetime.today().strftime('%d %b %Y')),
        #     message='',
        #     from_email=settings.EMAIL_HOST_USER,
        #     recipient_list=['yash.yadav@zopper.com','yashu.deepyadav@gmail.com']
        # )


        from django.core import mail
        from django.template.loader import render_to_string
        from django.utils.html import strip_tags

        email_subject = "Claim Report for {}".format(datetime.today().strftime('%d %b %Y')),
        html_message = render_to_string('email.html', email_attachment_template_context)
        plain_message = strip_tags(html_message)
        from_email=settings.EMAIL_HOST_USER
        to = ['yash.yadav@zopper.com','yashu.deepyadav@gmail.com']

        mail.send_mail(email_subject, plain_message, from_email, to, html_message=html_message)







AutoReport()