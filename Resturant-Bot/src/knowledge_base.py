import json
from typing import Dict, List, Any

class RestaurantKnowledgeBase:
    """Loads and searches the restaurant menu JSON"""
    
    def __init__(self, json_path: str):
        with open(json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.restaurant_name = self.data['restaurant']['name']
        self.services = self.data['restaurant']['services']
        self.payment_methods = self.data['payment_methods']
        self.menu = self.data['menu']
        self.deals = self.data['deals']
    
    def search_menu_item(self, query: str) -> List[Dict[str, Any]]:
        """Search for menu items by name or description"""
        query_lower = query.lower()
        results = []
        
        # Search in pizzas
        if 'Pizza' in self.menu:
            for category, items in self.menu['Pizza'].items():
                for item in items:
                    if isinstance(item, dict) and 'name' in item:
                        if query_lower in item['name'].lower() or \
                           (query_lower in item.get('description', '').lower()):
                            results.append({
                                'category': f'Pizza - {category}',
                                **item
                            })
        
        # Search in other menu categories
        for category, items in self.menu.items():
            if category == 'Pizza':
                continue
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict) and 'name' in item:
                        if query_lower in item['name'].lower() or \
                           (query_lower in item.get('description', '').lower()):
                            results.append({
                                'category': category,
                                **item
                            })
        
        return results
    
    def get_category_items(self, category: str) -> List[Dict[str, Any]]:
        """Get all items in a category"""
        results = []
        category_lower = category.lower()
        
        if 'pizza' in category_lower:
            if 'Pizza' in self.menu:
                for subcategory, items in self.menu['Pizza'].items():
                    for item in items:
                        if isinstance(item, dict):
                            results.append({
                                'category': f'Pizza - {subcategory}',
                                **item
                            })
        else:
            for cat_name, items in self.menu.items():
                if category_lower in cat_name.lower():
                    if isinstance(items, list):
                        for item in items:
                            if isinstance(item, dict):
                                results.append({
                                    'category': cat_name,
                                    **item
                                })
        
        return results
    
    def get_deals(self) -> Dict[str, Any]:
        """Get all available deals"""
        return self.deals
    
    def get_restaurant_info(self) -> str:
        """Get basic restaurant information"""
        return f"""
Restaurant: {self.restaurant_name}
Services: {', '.join(self.services)}
Payment Methods: {', '.join(self.payment_methods)}
        """.strip()