import requests
from models import Items, Feedback
import csv
import re
from db.models import Product
from db.database import SessionLocal


class ParseWB:
    def __init__(self, url: str):
        self.seller_id = self.__get_seller_id(url)
        
    def __get_item_id(self, url:str):
        regex = "(?<=catalog/).+(?=/detail)"
        item_id = re.search(regex, url)[0]
        return item_id
        

    def __get_seller_id(self, url):
        response = requests.get(f'https://card.wb.ru/cards/v1/detail?nm={self.__get_item_id(url=url)}')
        seller_id = Items.model_validate(response.json()['data'])
        return seller_id.products[0].supplierId
    
    def parse(self):
        _page = 1
        self.__create_csv()
        
        while True:
            response = requests.get(f'https://catalog.wb.ru/sellers/catalog?dest=-1257786&supplier={self.seller_id}&page={_page}')
            response.raise_for_status()
            _page +=1
            items_info = Items.model_validate(response.json()['data'])
            print(items_info)
            if not items_info.products:
                break
            self.__feedback(items_info)
            self.__safe_csv(items_info)
            self.__save_to_db(items_info)
            
            
            
            
    @staticmethod
    def  __create_csv():
        with open('data_wb.csv', mode ='w', newline='')as file:
            writer = csv.writer(file)
            writer.writerow(
                ['id', 'наименование', 'price', 'brand', 'скидка', 'rating', 'вналичии', 'seller id', 'колличество отзывов', 'оценка']
            )
            
    @staticmethod
    def __safe_csv(items: Items):
        with open('data_wb.csv', mode='a', newline='')as file:
            writer= csv.writer(file)
            for product in items.products:
                writer.writerow([product.id,
                                 product.name,
                                 product.salePriceU,
                                 product.brand,
                                 product.sale,
                                 product.rating,
                                 product.volume,
                                 product.supplierId,
                                 product.feedback_count,
                                 product.valuation])        
            

    @staticmethod
    def __feedback(item_model: Items):
        for product in item_model.products:
            url = f'https://feedbacks2.wb.ru/feedbacks/v1/{product.root}'
            res = requests.get(url=url)
            if res.status_code ==200:
                feedback = Feedback.model_validate(res.json())
                product.feedback_count = feedback.feedbackCountWithText
                product.valuation = feedback.valuation
        
    @staticmethod       
    def __save_to_db(items:Items):
        session = SessionLocal()
        try:
            for product in items.products:
                db_product = Product(
                    name=product.name,
                    price=product.salePriceU,
                    brand=product.brand,
                    discount=product.sale,
                    rating=product.rating,
                    volume=product.volume,
                    supplier_id=product.supplierId,
                    feedback_count=product.feedback_count,
                    valuation=product.valuation,        
                )
                session.add(db_product)
            session.commit()
        except Exception as e:
            print(f'error:[{e}]')
        finally:
            session.close()
        



        
if __name__ == '__main__':
    ParseWB('https://www.wildberries.ru/catalog/17334044/detail.aspx').parse()











