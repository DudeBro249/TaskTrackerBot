from typing import Any, Dict
from sqlalchemy import Table
from sqlalchemy.sql.selectable import Select

def build_query(table: Table, filters: Dict[str, Dict[str, Any]]=None) -> list:
    query: Select = table.select()
    values = {}

    if filters:
        if filters.get('equalTo') != None:
            for filter in filters['equalTo'].keys():
                if filters['equalTo'].get(filter) != None:
                    query = query.where(getattr(table.c, filter) == '')
                    values[filter + '_1'] = filters['equalTo'].get(filter)

        if filters.get('lessThan') != None:
            for filter in filters['lessThan'].keys():
                if filters['lessThan'].get(filter) != None:
                    query = query.where(getattr(table.c, filter) <= '')
                    values[filter + '_1'] = filters['lessThan'].get(filter)

        if filters.get('greaterThan') != None:
            for filter in filters['greaterThan'].keys():
                if filters['greaterThan'].get(filter) != None:
                    query = query.where(getattr(table.c, filter) >= '')
                    values[filter + '_1'] = filters['greaterThan'].get(filter)
    
    if values == {}:
        values = None
    return str(query), dict(values)