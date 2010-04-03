"""
Alpha Paginator module
"""
from django.core.paginator import Paginator
from django.db import connection

class AlphaPaginator(Paginator):
    """
    Extention on Django core paginator to allow pagination by the first letter of
    a specified field (which defaults to 'name') of the given model
    """
    
    def __init__(self, *args, **kwargs):
        """
        Override Paginator.__init__ to also take the parameter 'field'
        @param field: The field by which to alphabetically organize the pages.  Defaults to 'name'
        """
        self.field = kwargs.get('field', 'name')
        super(AlphaPaginator, self).__init__(*args, **kwargs)
    
    def page(self, number):
        """
        Override Paginator.page to accept strings
        if the string isn't a number, it will take the first letter, and find
        the first page with an object matching that letter
        """
        num_str = str(number)
        if num_str.isdigit():
            number = int(num_str)
        else: #fetch page by first letter of configured field
            letter = num_str[0].lower()
            alpha_index = self.object_list.filter(name__lt=letter).count()
            number = (alpha_index/self.per_page)+1
        
        number = min(max(number, 1), self.num_pages)
        return super(AlphaPaginator, self).page(number)
    
    def alphabet(self):
        """
        @return: A list containing all of the first letters (capitalized) available
        in the objects list.
        """
        sql = """
        SELECT DISTINCT UPPER(SUBSTRING({field},1,1)) 
        FROM {table} order by {field};
        """
        cursor = connection.cursor()
        query = sql.format(table=self.object_list.model._meta.db_table,
                           field=self.field)
        cursor.execute(query)
        alphabet = [a[0] for a in cursor.fetchall()]
        return alphabet
