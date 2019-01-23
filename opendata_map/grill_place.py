class grill_historics():
    measurements:list

    def __init__(self):
        self.measurements = [[]]

    def operate_on_grill_history(self,grill,function):
        for items in self.measurements:
            if items:
                if items[0]['id'] == grill['id']:
                    return function(grill, items)


    def append(self,grill):
        for items in self.measurements:
            if items:
                if 'id' in grill and items[0]['id'] == grill['id']:
                    items.append(grill)
        else:
                self.measurements.append([grill])


    def get_grill(self,grill_id):
       for items in self.measurements:
           if items:
               if items[0]['id'] == grill_id:
                   return items[0]


    def get_heads(self):
        temp = []
        for items in self.measurements:
            if items:
                temp.append(items[0])
        return temp

    def get_history(self,grill):
        func = lambda grill, items: items
        return self.operate_on_grill_history(grill,func)
