
class DataValidator:
    

    def is_valid_product(self, item):

        required_fields = ['_id', 'stock_code', 'name','price','status']
        return all(item.get(field) for field in required_fields)
    