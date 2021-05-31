import requests
from bs4 import BeautifulSoup
import datetime
class Amazon():
    def __init__(self,urun_adi,kullanilacak_para_birimi,minimum_para,maksimum_para):
        self.urun_adi=urun_adi
        self.headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
        self.liste=[]
        self.kullanilacak_para_birimi=kullanilacak_para_birimi
        self.minimum_para=minimum_para
        self.maksimum_para=maksimum_para

    def exchange_converter(self,from_money):
        url = 'https://api.exchangerate.host/convert?from='+from_money+'&to='+self.kullanilacak_para_birimi
        while True:
            try:
                response = requests.get(url)
                data = response.json()
                break 
            except:
                pass
        return data["result"]
     
    def url(self,uzanti):
        main_url="https://www.amazon"+uzanti
        url=main_url+"/s?k="+self.urun_adi+"&ref=nb_sb_noss_1"
        return main_url,url

    def add_list(self,urun_basligi,urun_linki,fiyat,ulke,para_birimi):
        urun_bilgileri={
            "amazon":ulke,
            "baslik":urun_basligi,
            "fiyat":fiyat,
            "link":urun_linki,
            "para":para_birimi
        }
        self.liste.append(urun_bilgileri)

    def soup(self,class_name,url):
        deneme_sayisi=0
        while True:
            try:
                deneme_sayisi=deneme_sayisi+1
                r = requests.get(url, headers=self.headers)
                content = r.content
                soup = BeautifulSoup(content,features="lxml")
                a=soup.findAll('div', attrs={'class':class_name})
                if a !=[] or deneme_sayisi==5:
                    break
            except:
                pass
        
        return a

    def add_product_info(self,main_url,a,ulke,para_birimi):
        for i in a:
            try:
                urun_basligi=i.h2.text
                urun_linki=main_url+i.findAll('a')[0]['href']
                fiyat=i.find("span",{"class":"a-price-whole"}).text.replace(",",".")[:-1]
                ondalik=i.find("span",{"class":"a-price-fraction"}).text
                son_fiyat=fiyat+"."+ondalik
                nokta_sayisi=0
                for i in son_fiyat:
                    if i==".":
                        nokta_sayisi=nokta_sayisi+1
                        
                if nokta_sayisi==2:
                    son_fiyat=son_fiyat.split(".")
                    son_fiyat=float(son_fiyat[0]+son_fiyat[1]+"."+son_fiyat[2])
                else:
                    son_fiyat=float(son_fiyat)
                self.add_list(urun_basligi,urun_linki,son_fiyat,ulke,para_birimi)
            except :
                pass

    def amazon_au(self):        
        main_url,url=self.url(".com.au")
        a=self.soup('a-section a-spacing-medium',url)
        self.add_product_info(main_url,a,"au","USD")
        return self.liste
    
    def amazon_se(self):
        main_url,url=self.url(".se")
        a=self.soup('a-section a-spacing-medium',url)
        self.add_product_info(main_url,a,"se","SEK")
            
        return self.liste
       
    def amazon_es(self):
        main_url,url=self.url(".es")
        a=self.soup('a-section a-spacing-medium',url)
        self.add_product_info(main_url,a,"es","ESP")       
        return self.liste

    def amazon_pl(self):
        main_url,url=self.url(".pl")
        a=self.soup('a-section a-spacing-medium',url)
        self.add_product_info(main_url,a,"pl","PLN")
        
        return self.liste      

    def amazon_nl(self):
        main_url,url=self.url(".nl")
        a=self.soup('a-section a-spacing-medium',url)
        self.add_product_info(main_url,a,"nl","EUR")
        
        return self.liste

    def amazon_it(self):
        main_url,url=self.url(".it")
        a=self.soup('a-section a-spacing-medium',url)
        self.add_product_info(main_url,a,"it","ITL") 
        return self.liste     

    def amazon_de(self):
        main_url,url=self.url(".de")
        a=self.soup('a-section a-spacing-medium',url)
        self.add_product_info(main_url,a,"de","EUR")
        
        return self.liste

    def amazon_fr(self):
        main_url,url=self.url(".fr")
        a=self.soup('a-section a-spacing-medium',url)
        self.add_product_info(main_url,a,"fr","EUR") 
        
        return self.liste  
    
    def amazon_sa(self):
        main_url,url=self.url(".sa")
        a=self.soup('a-section a-spacing-medium',url)
        for i in a:
            try:
                urun_basligi=i.h2.text
                urun_linki=main_url+i.findAll('a')[0]['href']
                fiyat=i.find("span",{"class":"a-price-whole"}).text.replace(",",".")[:-2]
                ondalik=i.find("span",{"class":"a-price-fraction"}).text
                son_fiyat=fiyat+"."+ondalik
                nokta_sayisi=0
                for i in son_fiyat:
                    if i==".":
                        nokta_sayisi=nokta_sayisi+1
                        
                if nokta_sayisi==2:
                    son_fiyat=son_fiyat.split(".")
                    son_fiyat=float(son_fiyat[0]+son_fiyat[1]+"."+son_fiyat[2])
                else:
                    son_fiyat=float(son_fiyat)
                self.add_list(urun_basligi,urun_linki,son_fiyat,"sa","SAR")
            except :
                pass
        
        return self.liste

    def amazon_ae(self):
        main_url,url=self.url(".ae")
        a=self.soup('a-section a-spacing-medium',url)
        self.add_product_info(main_url,a,"ae","AED")
                
        return self.liste

    def amazon_sg(self):
        main_url,url=self.url(".sg")
        a=self.soup('a-section a-spacing-medium',url)
        self.add_product_info(main_url,a,"sg","SGD")
        
        return self.liste

    def amazon_jp(self):
        main_url,url=self.url(".co.jp")
        a=self.soup('a-section a-spacing-medium',url)
        for i in a:
            try:
                urun_basligi=i.h2.text
                urun_linki=main_url+i.findAll('a')[0]['href']
                fiyat=i.find("span",{"class":"a-price-whole"}).text.replace(",","")[1:]
                fiyat=float(fiyat)
                self.add_list(urun_basligi,urun_linki,fiyat,"jp","JPY")
            except:
                pass     
        
        return self.liste
            
    def amazon_in(self):
        main_url,url=self.url(".in")
        a=self.soup('s-include-content-margin s-border-bottom s-latency-cf-section',url)
        for i in a:
            try:
                urun_basligi=i.h2.text
                urun_linki=main_url+i.findAll('a')[0]['href']
                fiyat=i.find("span",{"class":"a-price-whole"}).text.replace(",",".")
                fiyat=float(fiyat)
                self.add_list(urun_basligi,urun_linki,fiyat,"in","INR")
            except:
                pass         
        
        return self.liste
    
    def amazon_cn(self):
        main_url,url=self.url(".cn")
        a=self.soup('s-expand-height s-include-content-margin s-border-bottom s-latency-cf-section',url)
        self.add_product_info(main_url,a,"CN","CNY")            
        return self.liste
        
    def amazon_mx(self):
        main_url,url=self.url(".com.mx")
        a=self.soup('s-expand-height s-include-content-margin s-border-bottom s-latency-cf-section',url)          
        self.add_product_info(main_url,a,"mx","MXN")  
        
        return self.liste 
    
    def amazon_tr(self):
        main_url,url=self.url(".com.tr")
        a=self.soup('s-expand-height s-include-content-margin s-border-bottom s-latency-cf-section',url)        
        self.add_product_info(main_url,a,"tr","TRY")
        
        return self.liste
    
    def amazon_br(self):
        main_url,url=self.url(".com.br")
        a=self.soup('s-expand-height s-include-content-margin s-border-bottom s-latency-cf-section',url)
        self.add_product_info(main_url,a,"br","BRL")
            
        return self.liste
    
    def main(self):
        print("Amazon AU Taranıyor.")
        self.amazon_au()
        print("Amazon SE Taranıyor.")
        self.amazon_se()
        print("Amazon ES Taranıyor.")
        self.amazon_es()
        print("Amazon PL Taranıyor.")
        self.amazon_pl()
        print("Amazon NL Taranıyor.")
        self.amazon_nl()
        print("Amazon IT Taranıyor.")
        self.amazon_it()
        print("Amazon DE Taranıyor.")
        self.amazon_de()
        print("Amazon FR Taranıyor.")
        self.amazon_fr()
        print("Amazon SA Taranıyor.")
        self.amazon_sa()
        print("Amazon AE Taranıyor.")
        self.amazon_ae()
        print("Amazon SG Taranıyor.")
        self.amazon_sg()
        print("Amazon JP Taranıyor.")
        self.amazon_jp()
        print("Amazon IN Taranıyor.")
        self.amazon_in()
        print("Amazon CN Taranıyor.")
        self.amazon_cn()
        print("Amazon MX Taranıyor.")
        self.amazon_mx()
        print("Amazon TR Taranıyor.")
        self.amazon_tr()
        print("Amazon BR Taranıyor.")
        self.amazon_br()
        for urun in self.liste:
            ulke=urun["amazon"]
            baslik=urun["baslik"]
            fiyat=urun["fiyat"]
            link=urun["link"]
            para_birimi=urun["para"]
            counter=0
            for a in self.urun_adi.split("+"):
                if a in baslik.lower():
                    counter=counter+1
                    
            if counter==len(self.urun_adi.split("+")): #doğru ürün 
                kur=self.exchange_converter(para_birimi)
                if fiyat*kur>self.minimum_para and fiyat*kur<self.maksimum_para:                
                    print(fiyat*kur,baslik,link)

                 
                
aranacak_kelime=input("Aramak İstediğiniz Ürün Adını Yazınız:")
cevrilecek_para_birimi=input("Hangi Para Birimini Kullanmak İstersiniz(TRY/EUR/USD):")
minimum_deger=int(input("Ürünün Minimum Değerini Giriniz:"))
maksimum_deger=int(input("Ürünün Maksimum Değerini Giriniz:"))
print(datetime.datetime.now())
aranacak_kelime=aranacak_kelime.replace(" ","+")  
a=Amazon(aranacak_kelime,cevrilecek_para_birimi.upper(),minimum_deger,maksimum_deger)
d=a.main()
print(datetime.datetime.now())
